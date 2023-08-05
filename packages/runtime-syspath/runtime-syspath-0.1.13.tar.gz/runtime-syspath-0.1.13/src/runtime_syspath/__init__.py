# pylint: disable=invalid-name
""" __init__ module. """
import re

# noinspection PyUnresolvedReferences
# pylint: disable=import-error
from .syspath_utils import (  # noqa
    add_srcdirs_to_syspath,
    filtered_sorted_syspath,
    get_package_and_max_relative_import_dots,
    init_std_syspath_filter,
    print_syspath,
)

# pylint: enable=import-error

__version__ = "0.1.13"

init_std_syspath_filter(re.compile(r"([Jj]et[Bb]rains|[Pp]ython|PyCharm|v\w*env)"))
