from packaging.version import Version

PROJECT = "simplearg"
VERSION = Version("0.0.1.alpha.0")


def get_version():
    return str(VERSION)
