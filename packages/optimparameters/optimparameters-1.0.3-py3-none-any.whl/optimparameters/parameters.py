import numpy as np
from pdb import set_trace as stop

class Parameter:
    
    """A class for a model parameter. The hard bounds and uncertainty are meant to effectively implement uniform and Gaussian priors.

    Attributes:
        name (str): The name of the parameter.
        value (str): The current value of the parameter.
        minv (str): The min bound.
        maxv (str): The max bound.
        vary (str): Whether or not to vary this parameter.
        mcmcscale (str): The mcmc scale step of the parameter.
        commonality (str): What this parameter is common to. Can be anything the user decides to implement.
    """
    
    default_keys = ('name', 'value', 'minv', 'maxv', 'vary', 'mcmcscale', 'commonality', 'uncertainty')

    def __init__(self, name=None, value=None, minv=-np.inf, maxv=np.inf, vary=True, mcmcscale=None, commonality=None, uncertainty=None):
        """Creates a Parameter object.

        Args:
            name (str): The name of the parameter.
            value (Number): The value of the parameter.
            minv (Number): The min bound.
            maxv (Number): The max bound.
            vary (bool): Whether or not to vary this parameter.
            mcmcscale (float): The mcmc scale step of the parameter.
            commonality (str): What this parameter is common to. Can be anything the user decides to implement.
            uncertainty (Number): Any uncertaintyertainty. Typically only relevant after updates.
        """
        
        # Set all attributes
        self.name = name
        self.value = value
        self.minv = minv
        self.maxv = maxv
        self.vary = vary
        self.mcmcscale = mcmcscale
        self.commonality = commonality
        self.uncertainty = uncertainty

    def __repr__(self):
        s = '(Parameter)  Name: ' + self.name + ' | Value: ' + str(self.value)
        if not self.vary:
            s +=  ' (Locked)'
        
        s +=  ' | Bounds: [' + str(self.minv) + ', ' + str(self.maxv) + ']'
        
        if self.uncertainty is not None:
            s += ' | Uncertainty: ' + str(self.uncertainty)
        if self.mcmcscale is not None:
            s += ' | MCMC scale: ' + str(self.mcmcscale)
        if self.commonality is not None:
            s += ' | Commonality: ' + str(self.commonality)
        return s
    
    def setv(self, **kwargs):
        """Setter method for the attributes.

        kwargs: Any available atrributes.
        """
        for key in kwargs:
            setattr(self, key, kwargs[key])
        

class Parameters(dict):
    """A container for a set of model parameters which extends the Python 3 dictionary, which is ordered by default.
    """
    
    default_keys = Parameter.default_keys

    def __init__(self):
        
        # Initiate the actual dictionary.
        super().__init__()
            
            
    @classmethod
    def from_numpy(cls, **kwargs):
        """Create a parameters object from numpy arrays
        
        kwargs:
            Iterables of parameter attributes.
        """
        pars = cls()
        n = len(kwargs['value'])
        if 'name' in kwargs:
            names = kwargs['name']
        else:
            names = ['par' + str(i + 1) for i in range(n)]
            
        for ipname, pname in enumerate(names):
            par_kwargs = {}
            par_kwargs['name'] = pname
            par_kwargs['value'] = kwargs['value'][ipname]
            for ikey, kw in enumerate(kwargs):
                if kwargs[kw] is not None and kw not in par_kwargs:
                    par_kwargs[kw] = kwargs[kw][ikey]
            pars.add_parameter(Parameter(**par_kwargs))
        return pars
          
            
    def add_parameter(self, parameter):
        """Adds a parameter to the Parameters dictionary.

        Args:
            parameter (Parameter): The parameter to add.
        """
        self[parameter.name] = parameter
            
    def unpack(self, keys=None):
        """Unpacks values to numpy arrays.

        Args:
            keys (iterable or string): A tuple of strings containing the keys to unpack, defaults to None for all keys.
            
        Returns:
            vals (dict): A dictionary containing the returned values.
        """
        if keys is None:
            keys = self.default_keys
        else:
            if type(keys) is str:
                keys = [keys]
        out = {}
        for key in keys:
            out[key] = np.array([getattr(self[pname], key) for pname in self])
        return out
            
    def pretty_print(self):
        """Prints all parameters and attributes in a readable fashion.
        """
        for key in self.keys():
            print(self[key], flush=True)
            
    
    def setv(self, **kwargs):
        """Setter method for an attribute(s) for all parameters, in order of insertion.

        kwargs:
            Any available Parameter atrribute.
        """
        
        for key in kwargs:
            vals = kwargs[key]
            for i, pname in enumerate(self):
                setattr(self[pname], key, vals[i])
        
    
    def sanity_lock(self):
        """Locks any parameters such that the min value is equal to the max value.
        """
        for pname in self:
            if self[pname].minv == self[pname].maxv:
                self[pname].vary = False
                
                
    def sanity_check(self):
        """Checks for parameters which vary and are out of bounds.
            Returns:
                bad_pars (list): A list containing parameter names (strings) which are out of bounds.
        """
        bad_pars = []
        for pname in self:
            v = self[pname].value
            vary = self[pname].vary
            minv = self[pname].minv
            maxv = self[pname].maxv
            if (v < minv or v > maxv) and vary:
                bad_pars.append(pname)
            
        return bad_pars
    
    def get_index(self, name):
        return list(self.keys()).index(name)
    
    def num_varied(self):
        nv = 0
        for pname in self:
            nv += int(self[pname].vary)
        return nv
    
    def num_locked(self):
        nl = 0
        for pname in self:
            nl += int(not self[pname].vary)
        return nl
    
    def get_varied(self):
        varied_pars = Parameters()
        for pname in self:
            if self[pname].vary:
                varied_pars.add_parameter(self[pname])
        return varied_pars
    
    def get_locked(self):
        locked_pars = Parameters()
        for pname in self:
            if not self[pname].vary:
                locked_pars.add_parameter(self[pname])
        return locked_pars
    
    def get_subspace(self, par_names=None, indices=None):
        sub_pars = Parameters()
        if par_names is not None:
            for pname in par_names:
                sub_pars.add_parameter(self[pname])
        else:
            par_names = list(self.keys())
            for k in indices:
                sub_pars.add_parameter(self[par_names[k]])
        return sub_pars
            
    def index_from_par(self, par_name):
        return list(self.keys()).index(par_name)
    
    def par_from_index(self, k):
        return self[list(self.keys())[k]]
    
    @classmethod
    def oflength(cls, n):
        """Returns a parameters object of some length with dummy names.
        
        Args:
            n (int): The number of parameters to add.
        Returns:
            bad_pars (list): A list containing parameter names (strings) which are out of bounds.
        """
        pars = cls()
        for i in range(n):
            pars.add_parameter(name='par' + str(i + 1), value=0)
        return pars