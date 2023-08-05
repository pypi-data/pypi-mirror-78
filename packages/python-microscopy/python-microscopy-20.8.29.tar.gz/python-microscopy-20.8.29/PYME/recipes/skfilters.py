# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 17:11:05 2015

@author: david
"""
from .base import register_module, ModuleBase, Filter
from .traits import Input, Output, Float, Enum, CStr, Bool, Int, _IntFloat
from scipy import ndimage


import numpy as np
import six
import skimage.filters as skf
import inspect

"""Automagically generate filter objects for all skimage filters"""

class SKFilter(Filter):
        #def __init__(self, **kwargs):
        #    pass
        
        def applyFilter(self, data, chanNum, frNum, im):
            ret =  getattr(skf, self._filtName)(data, **self.kwargs())
            if 'threshold' in self._filtName and np.isscalar(ret):
                #thresholding functions return the threshold value, not a mask
                #we want a mask
                return data > ret
            else:
                return ret
        
        def completeMetadata(self, im):
            im.mdh['Processing.' + self._filterID] = self._getargmd()
            
        def kwargs(self):
            return {an: getattr(self, an) for an in self._argnames}
            
        def _getargmd(self):
            return {an: repr(getattr(self, an)) for an in self._argnames}
            
ctemplate = """
@register_module("%(FilterID)s")
class %(FilterID)s(SKFilter):
    '''
    Autogenerated wrapper around `skimage.filters.%(filtName)s`

    From `skimage` documentation.
    -----------------------------

    Note that for threshold_functions, we return a thresholded image, **not** the threshold value.

    %(doc)s
    '''
    _argnames = args
    _filtName = "%(filtName)s"
    _filterID = "%(FilterID)s"
    
    %(paramString)s


"""

#print ctemplate

skFilterNames = [n for n in dir(skf) if inspect.isfunction(getattr(skf, n)) and not n.startswith('_')]


for filtName in skFilterNames:
    filt = getattr(skf, filtName)
    
    FilterID =  'SKF_' + filtName

    try:
        argspec = inspect.getfullargspec(filt)
    except AttributeError:  # python 2
        argspec = inspect.getargspec(filt)

    if len(argspec.args) > 0:
        args = argspec.args[1:]
        
        if len(args) > 0:
            argTypes = {a: 'int_float' for a in args}
            argDefaults = {a: 0.0 for a in args}
            
            #print filtName, argspec
            
            #work backwards through supplied defaults
            if not argspec.defaults is None:
                for j in (1 + np.arange(len(argspec.defaults))):
                    a = args[-j]
                    ad = argspec.defaults[-j]
                    argDefaults[a] = ad
                    if ad is None:
                        argTypes[a] = 'image'
                    elif isinstance(ad, six.string_types):
                        argTypes[a] = 'string'
                    elif isinstance(ad, dict):
                        argTypes[a] = 'dict'
                    elif isinstance(ad, bool):
                        argTypes[a] = 'bool'
                    elif isinstance(ad, int) and (ad != 0):
                        argTypes[a] = 'int'
            
            #disregard parameters which need another image for now        
            args = [a for a in args if not argTypes[a] in ['image', 'dict']]
            
            _argnames = args
        
        
        paramString = ''
                
        for a in args:
            if argTypes[a] == 'float':
                paramString += '%s = Float(%s)\n    ' % (a, argDefaults[a])
            elif argTypes[a] == 'string':
                paramString += '%s = CStr("%s")\n    ' % (a, argDefaults[a])
            elif argTypes[a] == 'bool':
                paramString += '%s = Bool(%s)\n    ' % (a, argDefaults[a])
            elif argTypes[a] == 'int':
                paramString += '%s = Int(%s)\n    ' % (a, argDefaults[a])
            elif argTypes[a] == 'int_float':
                paramString += '%s = _IntFloat(%s)\n    ' % (a, argDefaults[a])

        doc = filt.__doc__
                
        cd = ctemplate % locals()
        #print cd
        exec(cd)






 
#d = {}
#d.update(locals())
#moduleList = [c for c in d if _issubclass(c, ModuleBase) and not c == ModuleBase]       
