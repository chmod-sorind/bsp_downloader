usage: main.py [-h] [-l] [-r] [-d] [-c] URL

Download specified package from link/URL and installs it.

positional arguments:
  URL             The Link/URL to target package.

optional arguments:
  -h, --help      show this help message and exit
  -l, --log       Create Install Log.
  -r, --reboot    Reboot after install.
  -d, --dedicate  Run BSP dedication script upon installation.
  -c, --clean     Remove downloaded package after install.