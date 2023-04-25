from PyTexture.Orientation import Orientation
from numpy import eye

class Grain(Orientation):
    '''
    Grain is derived from the Orientation class.  In addition to the
    Orientation methods, this specifies grain-shape values (e.g., volume)
    '''


    def __init__(self,conv='passive',ortho=True, **kwargs):

        self.has_ortho_symm = ortho
        self.valid = True
        self.R = eye(3)
        self._conv = conv

        # Allow assignment of eulers when instantiating class
        if 'euler' in kwargs:
            self.fromEulerAngles(kwargs['euler'])
        # Process kwargs
        self.aspect_ratios = kwargs['aspect_ratios'] if 'aspect_ratios' in kwargs else None
        self.axis_lengths = kwargs['axis_lengths'] if 'axis_lengths' in kwargs else None
        self.centroid = kwargs['centroid'] if 'centroid' in kwargs else None
        self.volume = kwargs['volume'] if 'volume' in kwargs else None
        self.surface_feature = kwargs['surface_feature'] if 'surface_feature' in kwargs else None
        self.fip_max = kwargs['FIP_max'] if 'FIP_max' in kwargs else None
        self.delta_fip_max = kwargs['delta_FIP_max'] if 'delta_FIP_max' in kwargs else None