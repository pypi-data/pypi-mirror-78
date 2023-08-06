import sys

# import shortcuts
from pylinac import calibration
from pylinac.core import (
    decorators,
    geometry,
    image,
    io,
    mask,
    profile,
    roi,
    utilities,
)
from pylinac.core.utilities import assign2machine, clear_data_files
from pylinac.ct import CatPhan503, CatPhan504, CatPhan600, CatPhan604
from pylinac.flatsym import FlatSym
from pylinac.log_analyzer import Dynalog, MachineLogs, TrajectoryLog, load_log
from pylinac.picketfence import PicketFence  # must be after log analyzer
from pylinac.planar_imaging import (
    DoselabMC2kV,
    DoselabMC2MV,
    LasVegas,
    LeedsTOR,
    StandardImagingQC3,
)
from pylinac.py_gui import \
    gui  # must be after everything since it imports it all
from pylinac.starshot import Starshot
from pylinac.vmat import DRGS, DRMLC
from pylinac.watcher import process
from pylinac.winston_lutz import WinstonLutz

__version__ = '3.0.1.1'
__version_info__ = (3, 0, 1.1)

# check python version
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    raise ValueError("Pylinac is only supported on Python 3.6+. Please update your environment.")
