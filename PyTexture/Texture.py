
class Texture:


    ##############################################
    def __init__(self, ortho=True):
        '''
        The attributes here are the microstructure attributes you would find
        in the grain structure of a polycrystal.

        '''

        self.orientDict = {} # a dictionary of Orientation objects 
        self.eulerDict = {}
        self.rodDict = {}
        self.neighbors = {}
        self.otherNeighbors = {}
        self.misorient = {}
        self.primary_slip = {}
        self.mp = {}
        self.attrData = {}

        self.has_ortho_symm = ortho
        self.fromEulers = False
        self.fromRodrigues = False

    ##############################################
    def addGrain(self, grain_object, grain_name):
        '''
        add an Grain object to the Texture object
        
        grain_object = Grain object (currently, either FCCGrain or HCPGrain)
        grain_name = any hashable type to be used as dictionary key

        '''

        self.orientDict[grain_name] = grain_object