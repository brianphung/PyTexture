import pandas as pd
import numpy as np
from numpy import dot

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
        self.shared_area = {}
        self.additional_data = {}

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


    ##############################################
    def calc_mPrime(self, neighbors_only=False, grain_ids_start_at_zero=True):
        '''
        This function calculates the m' compatibility parameter for
        slip transmission (Luster & Morris).
        :return: None
        '''

        


        for orient1 in self.orientDict.keys():
            
            # find vecs
            cur_id = 'Grain_{}'.format(orient1 + 1) if grain_ids_start_at_zero else 'Grain_{}'.format(orient1)
            self.mp[cur_id] = []
            n1 = self.primary_slip[cur_id][1]  # normal of first slip system
            d1 = self.primary_slip[cur_id][2] # direction of first slip (Burger's vector)
            if neighbors_only:
                assert(grain_ids_start_at_zero == False), 'Only supports this'
                second_loop_orientation_list = self.neighbors[f'Grain_{orient1}']
            else:
                second_loop_orientation_list = self.orientDict.keys()
            for orient2 in second_loop_orientation_list:
                # find vecs
                other_id = 'Grain_{}'.format(orient2 + 1) if grain_ids_start_at_zero else 'Grain_{}'.format(orient2)
                n2 = self.primary_slip[other_id][1] # normal of second slip system
                d2 = self.primary_slip[other_id][2] # direction of second slip (Burger's vector)
                if (orient1 != orient2):
                    #rotate slip normal and direction to grain orientation
                    n1 = self.orientDict[orient1]._normalize(dot(self.orientDict[orient1].R,n1))
                    d1 = self.orientDict[orient1]._normalize(dot(self.orientDict[orient1].R,d1))
                    n2 = self.orientDict[orient2]._normalize(dot(self.orientDict[orient2].R,n2))
                    d2 = self.orientDict[orient2]._normalize(dot(self.orientDict[orient2].R,d2))

                    # check orthogonality
                    assert dot(n1,d1) < 1.0E-4, 'Grain vectors not orthogonal'
                    assert dot(n2,d2) < 1.0E-4, 'Neighbor vectors not orthogonal'

                    #phi
                    uv1 = n1 / np.linalg.norm(n1)
                    uv2 = n2 / np.linalg.norm(n2)
                    cos_phi = dot(uv1, uv2)

                    #kappa
                    uv1 = d1 / np.linalg.norm(d1)
                    uv2 = d2 / np.linalg.norm(d2)
                    cos_kappa = dot(uv1, uv2)

                    mp = cos_phi * cos_kappa
                    self.mp[cur_id].append(mp)
                else:
                    self.mp[cur_id].append(np.nan)

    ##############################################
    def export_pandas(self,features, **kwargs):
        ''' In an embarassingly inefficient manner, gather all grain
        data in a dictionary and export the data as a dataframe.
        
        features: a required keyword for features you want exported
        '''
        data = {}

        for feat in features:
            feature_list = []
            feat_length = 1
            # Do some preprocessing for mprime
            if 'mprime' in feat:
                if 'load_direction' not in kwargs:
                    raise Exception("If you're using mprime, defining load_direction is required!")
                if 'grain_ids_start_at_zero' not in kwargs:
                    raise Exception("If you're using mprime, defining grain_ids_start_at_zero is required!")
                for idx,theta in enumerate(self.orientDict):
                    cur_orient = self.orientDict[theta]
                    m,n,d = cur_orient.maxSchmidFactor(kwargs['load_direction'])
                    self.primary_slip['Grain_{}'.format(idx + 1)] = [m,n,d]
                # find min angle slip direction
                self.calc_mPrime(grain_ids_start_at_zero=kwargs['grain_ids_start_at_zero'], neighbors_only=True)

            for grain_id, grain_object in self.orientDict.items():
                # Check attributes that are part of the kwarg inputs
                if feat in grain_object.attributes:
                    if isinstance(grain_object.attributes[feat],(list,pd.core.series.Series,np.ndarray)):
                        if feat_length == 1:
                            for dummy in grain_object.attributes[feat]:
                                feature_list.append([])
                            feat_length = len(grain_object.attributes[feat])
                        for i, val in enumerate(grain_object.attributes[feat]):
                            feature_list[i].append(val)
                    else:
                        feature_list.append(grain_object.attributes[feat])
                elif feat == 'maxSchmidFactor':
                    if 'load_direction' not in kwargs:
                        raise Exception("If you're using maxSchmidFactor, defining load_direction is required!")
                    feature_list.append(grain_object.maxSchmidFactor(kwargs['load_direction'])[0])
                elif 'mprime' in feat:
                    if 'max' in feat:
                        feature_list.append(np.max(self.mp[f'Grain_{grain_id}']))
                    elif 'median' in feat:
                        feature_list.append(np.median(self.mp[f'Grain_{grain_id}']))
                    elif 'area' in feat:
                        max_area_idx = np.argmax(self.shared_area[f'Grain_{grain_id}'])
                        feature_list.append(self.mp[f'Grain_{grain_id}'][max_area_idx])
                    elif 'srest' in feat:
                        max_Wp_idx = np.argmax(self.additional_data['MaxWpAtGrainBoundary'][f'Grain_{grain_id}'])
                        feature_list.append(self.mp[f'Grain_{grain_id}'][max_Wp_idx])
                    else:
                        raise NotImplementedError
                elif feat == 'W_p_srest':
                    feature_list.append(np.max(self.additional_data['MaxWpAtGrainBoundary'][f'Grain_{grain_id}']))
                elif feat == 'misorientation':
                    max_Wp_idx = np.argmax(self.additional_data['MaxWpAtGrainBoundary'][f'Grain_{grain_id}'])
                    neighbor_max_Wp_gid =  self.neighbors[f'Grain_{grain_id}'][max_Wp_idx]
                    feature_list.append(grain_object.misorientation(self.orientDict[neighbor_max_Wp_gid]))                    
                else:
                    raise NotImplementedError(f'{feat} is not recognized.')
                

            if feat_length == 1:
                data[feat] = feature_list
            else:
                for i in range(feat_length):
                    data[f'{feat}_{i}'] = feature_list[i]

        


        return pd.DataFrame(data)