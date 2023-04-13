import configparser as cfp
import sys
from os.path import abspath, dirname, expanduser
from os.path import join as pjoin

if sys.platform == 'win32':
    HOME_INI = pjoin(expanduser('~'), '_dpkg', 'local.dsource')
else:
    HOME_INI = pjoin(expanduser('~'), '.dpkg', 'local.dsource')
SYS_INI = pjoin(abspath('etc'), 'dpkg', 'local.dsource')
OUR_PATH = dirname(__file__)
OUR_META = pjoin(OUR_PATH, 'meta.ini')
DISCOVER_INIS = {'user': HOME_INI, 'system': SYS_INI}


def main():
    # Get ini file to which to write
    try:
        reg_to = sys.argv[1]
    except IndexError:
        reg_to = 'user'
    if reg_to in ('user', 'system'):
        ini_fname = DISCOVER_INIS[reg_to]
    else:  # it is an ini file name
        ini_fname = reg_to

    # Read parameters for our distribution
    meta = cfp.ConfigParser()
    files = meta.read(OUR_META)
    if len(files) == 0:
        raise RuntimeError('Missing meta.ini file')
    name = meta.get('DEFAULT', 'name')
    version = meta.get('DEFAULT', 'version')

    # Write into ini file
    dsource = cfp.ConfigParser()
    dsource.read(ini_fname)
    if not dsource.has_section(name):
        dsource.add_section(name)
    dsource.set(name, version, OUR_PATH)
    dsource.write(file(ini_fname, 'wt'))

    print(f'Registered package {name}, {version} to {ini_fname}')


if __name__ == '__main__':
    main()
