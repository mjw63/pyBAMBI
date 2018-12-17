"""Keras neural net predictor.

This implements a Keras Sequential model (a deep MLP)

Author: Martin White (martin.white@adelaide.edu.au)
Date: December 2018

"""
import numpy
from pybambi.neuralnetworks.base import Predictor
from keras.models import Sequential
from keras.layers import Dense

class KerasNetInterpolation(Predictor):
    """ Keras neural net interpolation
    
    Returns the loglikelihood from a Keras neural net-based interpolator

    """

    def __init__(self, params, logL):
        super(KerasNetInterpolation, self).__init__(params, logL)
        self._params = params[:]
        self._logL = logL[:]

        # This function takes a parameter set, trains a neural net and returns the interpolated likelihood
        # It is intended to be cannibalised for later pyBAMBI functionality
        
        # Number of neurons in each hidden layer, could make this configurable?
        numNeurons = 200
        
        # Shuffle the params and logL in unison (important for splitting data into training and test sets)
        randomize = numpy.arange(len(self._params))
        numpy.random.shuffle(randomize)
        params = self._params[randomize]
        logL = self._logL[randomize]

        # Now split into training and test sets
        # Use 80-20 split, could make this configurable?
        npoints = int(numpy.rint(0.8*numpy.shape(params)[0]))
        params_training, params_test = params[:npoints,:], params[npoints:,:]
        logL_training, logL_test = logL[:npoints], logL[npoints:]

        # Create model
        model = Sequential()

        # Get number of input parameters
        # Note: if params contains extra quantities (ndim+others), we need to change this
        n_cols = params.shape[1]

        # Add model layers, note choice of activation function (relu)
        # We will use 3 hidden layers and an output layer
        # Note: in a Dense layer, all nodes in the previous later connect to the nodes in the current layer

        model.add(Dense(numNeurons, activation='relu', input_shape=(n_cols,)))
        model.add(Dense(numNeurons, activation='relu'))
        model.add(Dense(numNeurons, activation='relu'))
        model.add(Dense(1))

        # Now compile the model
        # Need to choose training optimiser, and the loss function
        model.compile(optimizer='adam', loss='mean_squared_error')
        history = model.fit(params_training, logL_training, validation_data=(params_test,logL_test), epochs=100)
        
        self._model=model
        
                
    def __call__(self, x):
        x_ = numpy.atleast_2d(x)
        y = self._model.predict(x_)
        return numpy.squeeze(y)
