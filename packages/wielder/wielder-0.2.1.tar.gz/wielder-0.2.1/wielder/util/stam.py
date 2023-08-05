#!/usr/bin/env python
from wielder.util.commander import *
from wielder.util.log_util import setup_logging


if __name__ == "__main__":

    setup_logging(log_level=logging.DEBUG)

    _cmd = f'cd /Users/gideonbar/dev/dud; ' \
           f'coo="$(pwd)"; echo "im in $coo\n";' \
           f'$HOME/perl5/perlbrew/perls/perl-5.30.1/bin/perl  -I/Users/gideonbar/dev/dud/chemistry -I/Users/gideonbar/dev/dud/dao -I/Users/gideonbar/dev/dud/dispatch -I/Users/gideonbar/dev/dud/docking -I/Users/gideonbar/dev/dud/evolution -I/Users/gideonbar/dev/dud/genome -I/Users/gideonbar/dev/dud/hardcoded_dbs -I/Users/gideonbar/dev/dud/initializer -I/Users/gideonbar/dev/dud/util -I/Users/gideonbar/dev/dud/initializer /Users/gideonbar/dev/dud/scripts/dbIngestor.pl --env local --dest SOURCE_FILE'

    a = async_cmd(_cmd)

    for b in a:
        logging.debug(b)
