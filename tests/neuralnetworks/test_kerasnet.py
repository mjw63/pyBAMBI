import pytest
from pybambi.neuralnetworks.kerasnet import KerasNetInterpolation
import numpy

def test_KerasNet():

    # First, let's generate data from a 2D Gaussian

    # Pick some random numbers from a multivariate Gaussian (gives reasonable sampling density in the interesting regions)
    mu = numpy.array([0,0])
    sigma = 1
    Sigma = numpy.array([[sigma, 0], [0, sigma]])
    params = numpy.random.multivariate_normal(mu,Sigma,1000)

    # Now take those points and store log(function value) as the logL
    logL = []
    for x in params:
        logL.append((-x[0]*x[0]-x[1]*x[1]/(2*sigma*sigma))-numpy.log(numpy.sqrt(2*3.14*sigma*sigma)))
    logL = numpy.array(logL)
        
    # Initialise the keras net example, which includes training
    p = KerasNetInterpolation(params, logL)

    # Train the net and report back the interpolated value for this parameter set
    print "Checks of neural net interpolation"
    pred = p(params[0])
    print logL[0], pred
    pred = p(params[1])
    print logL[1], pred
    
    assert False
