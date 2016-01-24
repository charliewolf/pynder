import os

from six.moves.configparser import ConfigParser


FILE_DIR = os.path.dirname(__file__)


def read_test_ini(file_dir=FILE_DIR, section="FacebookAuth"):
    ini_file_path = os.path.join(file_dir, "test.ini")
    ret = {}
    if os.path.isfile(ini_file_path):
        cp = ConfigParser()
        cp.read(ini_file_path)
        if section not in cp.sections():
            raise EnvironmentError(
                "Section '{0}' not in test.ini".format(section))
        for arg in cp.options(section):
            ret[arg] = cp.get(section, arg)
    else:
        raise EnvironmentError(
            "File test.ini not existing in path '{0}'".format(FILE_DIR))
    return ret
