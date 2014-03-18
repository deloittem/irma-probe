import logging

from modules.antivirus.sophos import Sophos
from probes.antivirus.antivirus import AntivirusProbe


log = logging.getLogger(__name__)

class SophosProbe(AntivirusProbe):
    
    ##########################################################################
    # plugin metadata
    ##########################################################################

    _plugin_name = "Sophos"
    _plugin_version = "0.0.0"
    _plugin_description = "Antivirus plugin for Sophos Anti-Virus for Unix plugin CLI mode"

    ##########################################################################
    # constructor and destructor stuff
    ##########################################################################

    def __init__(self, conf=None, **kwargs):
        # call super classes constructors
        super(SophosProbe, self).__init__(conf, **kwargs)
        self._module = Sophos()