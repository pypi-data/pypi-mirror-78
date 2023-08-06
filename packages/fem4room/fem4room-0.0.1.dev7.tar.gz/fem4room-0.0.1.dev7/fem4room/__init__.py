from .Boundary import Boundary
from .Tools import Visualization,Sources,SaveLoad,Other
from .Simulation import Simulation
from .Solver import Solver
from .TimeEngine import Newmark,LeapFrog
"""Recommended: scikit-umfpack  (0.3.1 +)"""

global f4r_Umfpack_Available
try:
    import scikits.umfpack as umfpack
    f4r_Umfpack_Available = True
except ImportError:
    f4r_Umfpack_Available=False
