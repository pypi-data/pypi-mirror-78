from packaging.version import Version

PROJECT = "pieterraform"
VERSION = Version("0.0.1.alpha.8")


def get_version():
    return str(VERSION)
