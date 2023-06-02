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

        self.attributes = {}

        # Allow assignment of eulers when instantiating class
        if 'euler' in kwargs:
            self.fromEulerAngles(kwargs['euler'])
        # Define special kwargs that have specific functions
        attribute_kwargs = ['aspect_ratios', 'axis_lengths', 'centroid', 'volume',
                            'surface_feature', 'FIP_max', 'delta_FIP_max',
                            'quats', 'omega3', 'phases',
                            'applied_strain']

        # Process kwargs
        for kwarg_key, kwarg_value in kwargs.items():
            if kwarg_key in attribute_kwargs:
                self.attributes[kwarg_key] = kwarg_value
            else:
                self.attributes[kwarg_key] = None