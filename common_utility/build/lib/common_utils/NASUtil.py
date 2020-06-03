from common_utils.MLLogger import MLLogging
import configurations

logger=MLLogging.getLog()
"""
NAS also known as Network-Attached-Storage is a default Storage device. 
If not NAS, a simple local file system can be configured NAS.
"""
class NASConfiguration(object):
    """Initialize NAS Configuration Object from the project properties file"""
    def __init__(self):
        self.config = configurations.projectConfigurations.config
        if 'NAS' in self.config.keys():
            if 'NAS_local_folder_path' in self.config['NAS'].keys() and self.config['NAS']['NAS_local_folder_path'] is not None:
                self.nas_local_folder_path= self.config['NAS']['NAS_local_folder_path']