import itertools
import tarfile
import zipfile
from pathlib import Path
from tempfile import mkdtemp

import fire

from azureml.studio.core.io.any_directory import _META_FILE_PATH
from azureml.studio.core.io.image_directory import ImageDirectory
from azureml.studio.core.logger import logger
from azureml.studio.internal.error import ErrorMapping, InvalidDatasetError
from azureml.studio.internal.error_handler import error_handler

# This mapping is used for handling compressed files
COMPRESSED_EXT_TO_METHOD = {
    '.zip': zipfile.ZipFile,
    # do not use class 'tarfile.TarFile' directly but tarfile.open() instead
    # based on https://docs.python.org/3/library/tarfile.html
    '.tar': tarfile.open,
    '.gz': tarfile.open,
    '.bz2': tarfile.open,
}


def detect_base_dir_in_uncompressed(uncompressed_dir: Path):
    """Detect the real base directory containing images in an uncompressed directory.
    Recursively search if current directory contains only one directory. For example,
    aaa/xx.yaml => aaa
    aaa/aaa/xx.yaml => aaa/aaa
    If there is no subfolder, no _meta.yaml but all files in current directory, will return its parent path
    in order to get correct annotation which is saved as subfolder name in torchvision ImageFolder. For example,
    root/dog/*.png => root
    """
    def first_n_files(path, file_num=2):
        return list(itertools.islice(Path(path).iterdir(), file_num))

    def get_sub_dir_cnt(path):
        return len([x for x in path.iterdir() if x.is_dir()])

    base_dir = uncompressed_dir
    while True:
        files = first_n_files(base_dir)
        if not files:
            ErrorMapping.throw(
                InvalidDatasetError(dataset1=base_dir.name,
                                    reason=f"no file is found in '{base_dir}'",
                                    troubleshoot_hint="Please input a non-empty compressed file."))

        sub_dir_cnt = get_sub_dir_cnt(base_dir)
        logger.info(f"{sub_dir_cnt} subfolder(s) in current directory '{base_dir}'. List some files: {files}.")
        if sub_dir_cnt == 0 and not (base_dir / _META_FILE_PATH).exists():
            logger.info(f"No subfolder and no meta, use parent path '{base_dir.parent}' as"
                        " base directory for sake of annotation.")
            return base_dir.parent

        if len(files) == 1 and files[0].is_dir():
            logger.info(f"Only 1 folder is found in '{base_dir}', start searching the subfolder '{files[0]}'.")
            base_dir = files[0]
        else:
            logger.info(f"Detected real base directory path '{base_dir}'.")
            return base_dir


def extract_compressed_file_to_dir(compressed_file: Path):
    ext = compressed_file.suffix
    target_dir = Path(mkdtemp())
    with COMPRESSED_EXT_TO_METHOD[ext](compressed_file) as zf:
        zf.extractall(target_dir)
    logger.info(f"Extract compressed file to path '{target_dir}'.")
    target_dir = detect_base_dir_in_uncompressed(target_dir)
    return target_dir


def detect_image_directory_path(input_path: Path):
    """Detect target image directory path when walking through input path.

    :param input_path: Path
    :return: Path
    """
    target_dir = input_path
    if input_path.is_file():
        if input_path.suffix in COMPRESSED_EXT_TO_METHOD:
            logger.info(f"Input is a compressed file. Loading from {input_path}.")
            target_dir = extract_compressed_file_to_dir(input_path)
        else:
            ErrorMapping.throw(
                InvalidDatasetError(dataset1=input_path.name,
                                    reason=f"file extension '{input_path.suffix}' is not allowed",
                                    troubleshoot_hint="Please input compressed file with allowed extensions: "
                                    f"{set(COMPRESSED_EXT_TO_METHOD.keys())}."))
    else:
        # load from any valid compressed file in first layer of current directory.
        compressed_file_paths = list(
            itertools.islice((path for path in input_path.iterdir() if path.suffix in COMPRESSED_EXT_TO_METHOD), 1))
        if len(compressed_file_paths) > 0:
            logger.info(f"Found {len(compressed_file_paths)} compressed file(s) in current directory. "
                        f"Pick 1 file to load: '{compressed_file_paths[0]}'.")
            target_dir = extract_compressed_file_to_dir(compressed_file_paths[0])
        else:
            # try to load from current directory.
            logger.info(f"Loading from directory {input_path}.")

    return target_dir


@error_handler
def convert(input_path, output_path):
    input_path = Path(input_path)
    target_dir = detect_image_directory_path(input_path)
    try:
        loader_dir = ImageDirectory.load(target_dir)
        loader_dir.dump(output_path)
    except (FileNotFoundError, ValueError) as e:
        ErrorMapping.rethrow(
            e,
            InvalidDatasetError(dataset1=input_path.name,
                                reason=f"Got exception when loading: {ErrorMapping.get_exception_message(e)}",
                                troubleshoot_hint="Please make sure there is image in input dataset, see "
                                "https://aka.ms/aml/convert-to-image-directory for input image dataset requirement."))


if __name__ == '__main__':
    fire.Fire(convert)
