
import os

from . import analysis
from .analysis import *

from . import core
from .core import *

# from . import external
# from .external import *

# from . import geometry
# from .geometry import *

# from . import viz
# from .viz import *

from .io import *
from .misc import *
from .version import __version__


# Contents
__all__ = [
    'io',
    'include_dir',
    'misc',
    '__version__'
]

__all__.extend(analysis.__all__)
__all__.extend(core.__all__)
# __all__.extend(external.__all__)
# __all__.extend(geometry.__all__)
# __all__.extend(viz.__all__)

# Add include path
include_dir = os.path.abspath(__file__ + '/../../include')
