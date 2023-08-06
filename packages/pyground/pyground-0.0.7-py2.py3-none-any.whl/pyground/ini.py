"""
INI file format utilities. This format has its origins in Microsoft Windows from before
Windows NT, which began to move such configuration needs into the global "registry".

INI files are plain text, consisting of properties and values belonging to sections.
"""
from configparser import ConfigParser
from typing import Dict

from .json import marshall


@marshall.register
def marshall_config_parser(
    config_parser: ConfigParser, **options
) -> Dict[str, Dict[str, str]]:
    """
    As noted in the stdlib's docs, "the only bit of magic involves the `DEFAULT` section",
    which provides fallback behavior when looking up values for (section, key) pairs:
    if the section does not have such a key, it then tries the special "DEFAULT" section.
    """
    return {
        section_name: dict(section_proxy)
        for section_name, section_proxy in config_parser.items()
    }
