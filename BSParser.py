import argparse
import sys


# Override the default behavior of the error method
class BSParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

# Define arguments.
parser = BSParser(description='Download specified package from link/URL and installs it.')
parser.add_argument('url', metavar='URL', type=str, help='The Link/URL to target package.')
parser.add_argument('-l', '--log', action='store_true', help='Create Install Log.')
parser.add_argument('-r', '--reboot', action='store_true', help='Reboot after install.')
parser.add_argument('-d', '--dedicate', action='store_true', help='Run BSP dedication script upon installation.')
parser.add_argument('-c', '--clean', action='store_true', help='Remove downloaded package after install.')
args = parser.parse_args()
