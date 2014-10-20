#-*- coding: utf-8 -*-

import reversion



from alibrary.models.basemodels import *
from alibrary.models.artistmodels import *
from alibrary.models.releasemodels import *
from alibrary.models.mediamodels import *
from alibrary.models.labelmodels import *
from alibrary.models.playlistmodels import *
from alibrary.models.formatmodels import *
from alibrary.models.lookupmodels import *

from alibrary.models.refactoring import *


reversion.register(Media)
reversion.register(Release)
reversion.register(Artist)
reversion.register(Label)
