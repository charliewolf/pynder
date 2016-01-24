import sys

ver = sys.version_info

PY2 = (ver[0] == 2)
PY3 = (ver[0] == 3)

if PY2:
    import ConfigParser  # NOQA

elif PY3:
    import configparser as ConfigParser  # NOQA
