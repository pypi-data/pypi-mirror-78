#!/opt/util/oitnb/bin/python

"""

assumes that it starts in a temporary directory with two directories that can be converted

add to your .hgrc:

[extensions]
hgext.extdiff =

[extdiff]
cmd.omeld =

For use with git, this might work:

alias gomeld='git difftool --extcmd=omeld -y'

"""

import sys
import os


def main():
    # print('omeld:', os.getcwd(), sys.argv[1:])
    assert len(sys.argv) == 3, 'omeld: expecting two arguments'
    runs = 0
    for idx, arg in enumerate(sys.argv[1:]):
        assert os.path.exists(sys.argv[1]), f'omeld: parameter {idx}, cannot find "{arg}"'
        rp = os.path.realpath(arg)
        # check if you are on a temporary directory, so there is less chance to screw up
        if rp.startswith('/tmp/') or rp.startswith('/var/tmp/'):
            runs += 1
            os.system('oitnb -q ' + rp)
    if runs > 0:
        os.system('meld ' + ' '.join(sys.argv[1:]))
    else:
        print('could not run oitnb on "{}" or "{}"'.format(*sys.argv[1:]))


if __name__ == '__main__':
    main()
