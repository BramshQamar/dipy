#!/usr/bin/python
""" Classes and functions for fitting the correlation tensor model """

import warnings
import functools
import numpy as np
import scipy.optimize as opt

from dipy.reconst.base import ReconstModel
from dipy.reconst.dki import (
                                DiffusionKurtosisFit,

                            )

class CorrelationTensorModel(ReconstModel):
    """ Class for the Correlation Tensor Model
    """
    def __init__(self, gtab, fit_method="", *args, **kwargs): #not sure about the fit method yet
        """ Diffusion Kurtosis Tensor Model [1]

        Parameters
        ----------
        gtab : GradientTable class instance

        fit_method : str or callable


        args, kwargs : arguments and key-word arguments passed to the 
        fit_method.

        """

    def fit(self, data, mask=None):
        """ Fit method of the CTI model class

        Parameters
        ----------
        data : array
            The measured signal from one voxel.

        mask : array
            A boolean array used to mark the coordinates in the data that
            should be analyzed that has the shape data.shape[-1]

        """
        
    def cti_prediction(cti_params, gtab1, gtab2, S0 = 1):
    
    """Predict a signal given correlation tensor imaging parameters
    
    	Parameters
    	----------
      	cti_params: numpy.ndarray (...,43)
    		All parameters estimated from the correlation tensor model.
    		Paramters are ordered as follows:: 
    		
		1. Six independent elments of diffusion tensor.
		2. Twenty-One elements of the covariance tensor
		3. Fifteen elements of the kurtosis tensor 
	S0 : float or ndarray (optional)
            The non diffusion-weighted signal in every voxel, or across all
            voxels. Default: 1
            
        Returns
        -------
        S : ndarray 
            Simulated signal based on the CTI model: 
            
    """
    math ? : design_maatrix x cti_params
    #were not considering the kurtosis tensor while generating signals.
    #we need to specify gtab1 and gtab2 
    
 
    def predict(self, cti_params, S0=1.):  #created
    	"""Predict a signal for the CTI model class instance given parameteres
    	
    	Parameters: 
    	-----------
    	params: numpy.ndarray (...,43)
    		All parameters estimated from the correlation tensor model.
    		Paramters are ordered as follows:: 
    		
		1. Three diffusion tensor's eigenvalues
		2. Three lines of the eigenvector matrix each containing the
		first, second and third coordinates of the eigenvector
		3. Twenty-One elements of the covariance tensor
		4. Fifteen elements of the kurtosis tensor 
	S0 : float or ndarray (optional)
            The non diffusion-weighted signal in every voxel, or across all
            voxels. Default: 1
            
        Returns
        -------
        S : numpy.ndarray
            Signals.
 	""" 
        
        #S = qti_signal(self.gtab, D, C, S0)
        #return S #this is from covariance matrix
        #return dki_prediction(self.model_params, gtab, S0)
        #this is from dki module
   	return cti_prediction(cti_params, self.gtab, S0)
        
        

class CorrelationTensorFit(DiffusionKurtosisFit):

    """ Class for fitting the Diffusion Kurtosis Model """ 

    def __init__(self, model, model_params):
    
        """ Initialize a CorrelationTensorFit class instance.

        Since CTI is an extension of DKI, class instance is defined as subclass
        of the DiffusionKurtosis from dki.py

        Parameters
        ----------
        model : CorrelationTensorModel Class instance
            Class instance containing the Correlation Tensor Model for the fit
        model_params : ndarray (x, y, z, 27) or (n, 27)
            All parameters estimated from the correlation tensor model.
            Parameters are ordered as follows:

        """
        DiffusionKurtosisFit.__init__(self, model, model_params)
        
    def kt(self): #created
        """
        Return the 15 independent elements of the kurtosis tensor as an array
        """
        return self.model_params[..., 27:42] #last index won't get included....?
        
   def dft(self):  #created
    	"""
    	Returns the 6 independent elements of the diffusion tensor as an array
    	"""
    	return self.model_params[...,:6]
    
    
    def cvt(self): #created
    	"""
	Returns the 21 independent elements of the covariance tensor as an array
	"""
	return self.model_params[...,6:27]
#calculating the mean of the kurtosis tensor...?Needs to be modified...? 
    def mkt(self, min_kurtosis=-3./7, max_kurtosis=10): #imported (dki.py)
    	return mean_kurtosis_tensor(self.model_params, min_kurtosis,
                                    max_kurtosis)
   
    def cvt( __ ): #calculates the mean of all covariance parameters. required ? Formula ? 
    
#There are 4 (radial,mean,axial,fractional) do we have something similar for covariance in qti ? 

        
#we separate the kurtosis in 3 parts: isotropic+anisotropoic+microscopic. Do we need methods for this? : REFER VIDEO ON THIS
     def split_dk_cv_param(params):
     	r""" Extract the diffusion tensor eigenvalues, the diffusion tensor
    eigenvector matrix, and the 15 independent elements of the kurtosis tensor
    from the model parameters estimated from the DKI model

    Parameters
    ----------
    
    
    """
    
    
    
    
    
    
    
  def predict(self, gtab, S0=1.):  #created
    	"""Given a CTI model fit, predict the signal on the vertices of a gradient table 
    	
    	Parameters: 
    	-----------
    	params: numpy.ndarray (...,43)
    		All parameters estimated from the correlation tensor model.
    		Paramters are ordered as follows:: 
    		
		1. Three diffusion tensor's eigenvalues
		2. Three lines of the eigenvector matrix each containing the
		first, second and third coordinates of the eigenvector
		3. Twenty-One elements of the covariance tensor
		4. Fifteen elements of the kurtosis tensor 
	S0 : float or ndarray (optional)
            The non diffusion-weighted signal in every voxel, or across all
            voxels. Default: 1
            
        Returns
        -------
        S : numpy.ndarray
            Signals.
        """
        return cti_prediction(self.model_params, gtab, S0)
        
   
   
   
   
def params_to_cti_params(result, min_diffusivity = 0): 

    # Extracting the diffusion tensor parameters from solution
    DT_elements = result[:6]
    evals, evecs = decompose_tensor(from_lower_triangular(DT_elements),
                                    min_diffusivity=min_diffusivity)

    # Extracting covariance tensor parameters from solution
    CT_elements = result[6:27]

    # Extracting kurtosis tensor parameters from solution
    MD_square = evals.mean(0)**2
    KT_elements = result[27:42] / MD_square if MD_square else 0.*result[27:]

    # Write output
    cti_params = np.concatenate((evals, evecs[0], evecs[1], evecs[2],
                                 CT_elements, KT_elements), axis=0)

    return cti_params

def params_to_dki_params(result, min_diffusivity = 0): 
#takes kurtosis tensor parameters and returns a matrix 

def params_to_dti_params(result, min_diffusivity = 0): 

def params_to_cvt_params(result, min_diffusivity = 0):








def split_cti_params(cti_params): 
   r"""Extract the diffusion tensor eigenvalues, the diffusion tensor eigenvector matrix, and the 21 independent elements of the covariance tensor, and the 15 independent elements of the kurtosis tensor from the model parameters estimated from the CTI model 
   Parameters: 
    	-----------
    	params: numpy.ndarray (...,43)
    		All parameters estimated from the correlation tensor model.
    		Paramters are ordered as follows:: 
    		
		1. Three diffusion tensor's eigenvalues
		2. Three lines of the eigenvector matrix each containing the
		first, second and third coordinates of the eigenvector
		3. Twenty-One elements of the covariance tensor
		4. Fifteen elements of the kurtosis tensor 
	S0 : float or ndarray (optional)
            The non diffusion-weighted signal in every voxel, or across all
            voxels. Default: 1
            
        Returns
        -------
	dvt : Siz independent diffusion tensor elemnets 
        cvt : Twenty-one elements of the covariance tensor
        kt: Fifteen elemnets of the kurtosis tensor 
       
      """ 
     dvt = cti_params[...,:6]
     cvt = cti_params[...,6:27]
     kvt = cti_params[..., 27:42]
     return dvt, cvt, kvt 
     
     
def ls_fit_cti(design_matrix, data, inverse_design_matrix, weights = True, min_diffusivity = 0): 
r""" Compute the diffusion and kurtosis tensors using an ordinary or
    weighted linear least squares approach [1]_

    Parameters
    ----------
    design_matrix : array (g, 43)
        Design matrix holding the covariants used to solve for the regression
        coefficients.
    data : array (g)
        Data or response variables holding the data.
    inverse_design_matrix : array (43, g)
        Inverse of the design matrix.
    weights : bool, optional
        Parameter indicating whether weights are used. Default: True.
    min_diffusivity : float, optional
        Because negative eigenvalues are not physical and small eigenvalues,
        much smaller than the diffusion weighting, cause quite a lot of noise
        in metrics such as fa, diffusivity values smaller than `min_diffusivity`
        are replaced with `min_diffusivity`.

    Returns
    -------
    cti_params : array (43)
        All parameters estimated from the correlation tensor model for all N
        voxels. Parameters are ordered as follows:
            1) Six independent diffusion tensor elements.
            2) Twenty-One indpendent covariance tensor elements. eigenvectors.
            3) Fifteen elements of the kurtosis tensor.
 """ 
     # Set up least squares problem
    A = design_matrix
    y = np.log(data) #is the log transformation genuine??

    # CTI ordinary linear least square solution
    result = np.dot(inverse_design_matrix, y)

    # Define weights as diag(yn**2)
    if weights:
        W = np.diag(np.exp(2 * np.dot(A, result)))
        AT_W = np.dot(A.T, W)
        inv_AT_W_A = np.linalg.pinv(np.dot(AT_W, A))
        AT_W_LS = np.dot(AT_W, y)
        result = np.dot(inv_AT_W_A, AT_W_LS)

    # Write output
    cti_params = params_to_cti_params(result, min_diffusivity=min_diffusivity)

    return cti_params
   
           
        
        
common_fit_methods = {'WLS': ls_fit_cti, #weighted least squares
		      'OLS': ls_fit_cti #ordinary least squares
		     }      
        
        
        
        
        
        
        

