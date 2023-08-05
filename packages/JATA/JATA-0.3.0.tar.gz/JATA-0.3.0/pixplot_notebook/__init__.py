from __future__ import absolute_import
from pixplot_notebook.pixplot import process_images, parse

# specify version number
import pkg_resources
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:

    import pixplot

except BaseException as e:
    install('pixplot')
    import pixplot

    print("Success installing pixplot_notebook packages:)")

__version__ = pkg_resources.get_distribution('pixplot').version