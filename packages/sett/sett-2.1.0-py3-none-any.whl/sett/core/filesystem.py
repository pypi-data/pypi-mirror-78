import os
from typing import List, Iterator
from pathlib import Path
import warnings
from .error import UserError


def search_files_recursively(input_list: List[str]) -> Iterator[str]:
    """Recursively search for files and/or verify that files part of
    input_list really exist.

    :param input_list: list of files and directories to recursively search
        for files.
    :return: list of files and their absolute path.
    :raises UserError:
    """

    # Loop through all input path provided by the user. If the path is a
    # directory, search it recursively for files.
    for path in input_list:
        path_obj = Path(path).absolute()
        if path_obj.is_file():
            yield path_obj.as_posix()
        elif path_obj.is_dir():
            yield from (x.as_posix() for x in path_obj.rglob('*') if x.is_file())
        else:
            raise UserError(f"input path is not a valid file or directory: "
                            f"{path_obj.name}")


def check_file_read_permission(input_list: List[str]) -> None:
    """Verify the user has read permission on all files listed in input_list
    """
    no_read_permission = [x for x in input_list if not os.access(x, os.R_OK)]
    if no_read_permission:
        raise UserError(f"no read permission on input files:"
                        f"{', '.join(no_read_permission)}")


def delete_files(*files: str) -> None:
    """Delete the specified file(s) and catch error if deletion fails.
    :param files: paths of files to delete from disk.
    :raises UserError:
    """
    failed = []
    for f in files:
        if os.path.exists(f):
            try:
                os.unlink(f)
            except BaseException:
                failed.append(f)

    if failed:
        warnings.warn(f"Failed to delete file(s): {', '.join(failed)}. "
                      f"You have to take care of the clean up")


def form_output_tar_name(output_name: str) -> str:
    """Define the path + name of the output tarball file of the encrypt
    workflow. If output_name does not contain any path information, the
    output directory is set to the current working directory.
    :param output_name: name or path + name of output tarball.
    :return: path and name of the output tarball file.
    :raises UserError:
    """
    # Add '.tar' extension to output name if needed.
    if not output_name.endswith('.tar'):
        output_name = output_name + '.tar'

    # If output_name does not contain any path info, the output path is
    # set to the current working directory.
    basename = Path(output_name).name
    if basename == output_name:
        output_dir = Path.cwd()
    else:
        output_dir = Path(output_name).parent

    # Verify that user has write permission to output directory. We do this
    # check now because the procedure of compression + encryption can take
    # a long time and we want to be able to warn the user immediately.
    if not output_dir.is_dir():
        raise UserError(f"output directory does not exist: {output_dir}")
    if not os.access(output_dir.as_posix(), os.W_OK):
        raise UserError(f"no write permission on directory: {output_dir}")

    return output_dir.joinpath(basename).as_posix()
