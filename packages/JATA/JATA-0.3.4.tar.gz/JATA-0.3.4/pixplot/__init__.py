from __future__ import absolute_import
from pixplot.pixplot import process_images, parse
import subprocess
import sys
# specify version number
import pkg_resources
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# try:
#
#     import pixplot
#
# except BaseException as e:
#     install('pixplot')
#     import pixplot
#
#     print("Success installing pixplot packages:)")

__version__ = pkg_resources.get_distribution('JATA').version