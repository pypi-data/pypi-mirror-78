# flake8: noqa
from lml.loader import scan_plugins_regex
from moban_ansible._version import __author__, __version__

ANSIBLE_LIBRARIES = "^moban_ansible_.+$"
ANSIBLE_EXTENSIONS = [
    "moban_ansible.tests.files",
]


scan_plugins_regex(ANSIBLE_LIBRARIES, "moban", None, ANSIBLE_EXTENSIONS)
