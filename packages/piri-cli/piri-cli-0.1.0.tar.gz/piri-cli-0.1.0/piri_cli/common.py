from typing import Any, overload

from returns.result import ResultE, safe
from typing_extensions import Literal


@overload
def read_file(
    file_path: str, mode: Literal['r'],
) -> ResultE[str]:
    """When 'r' is supplied we return 'str'."""


@overload  # noqa: WPS440, F811
def read_file(
    file_path: str, mode: Literal['rb'],
) -> ResultE[bytes]:
    """When 'rb' is supplied we return 'bytes' instead of a 'str'."""


@overload  # noqa: WPS440, F811
def read_file(file_path: str, mode: str) -> ResultE[Any]:
    """Any other options might return Any-thing!."""


@safe  # noqa: WPS440, F811
def read_file(file_path: str, mode: str) -> Any:
    """Open the file and return its contents.

    :param file_path: path to the file to read.
    :type file_path: str

    :parm mode: read mode, r = read string, rb =read bytes.
    :type mode: str

    :return: Success[bytes], Success[str], Failure[Exception]
    :rtype: bytes, str
    """
    with open(file_path, mode) as data_file:
        return data_file.read()


@safe  # noqa: WPS440, F811
def write_file(raw_data: str, file_path: str) -> None:
    """Write file.

    :param raw_data: Data to write to file
    :type raw_data: str

    :param file_path: writes file to this path.
    :type file_path: str

    :return: Success[None], Failure[Exception]
    :rtype: Result
    """
    with open(file_path, 'w') as data_file:
        data_file.write(raw_data)
