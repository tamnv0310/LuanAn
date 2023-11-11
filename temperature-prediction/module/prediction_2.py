from tensorflow import keras
from pickle import load
import numpy
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

# load the model
def loadModel(product_id=None, model=None):
    return keras.models.load_model(dir_path+ '/models-py/'+model+'-'+product_id+'', custom_objects=None, compile=True, options=None)

# load the scaler with fit_transformed by the dataset
def loadScaler(product_id=None, model=None):
    return load(open(dir_path+ '/models-py/'+model+'-'+product_id+'/scaler.pkl', 'rb'))

#prediction function    
def predict_from_val(input=0, reconstructed_model=None, scaler=None):
    _input2d = numpy.array([[input]])

    #transform input by saved scaler
    _input_scaled2d = scaler.transform(_input2d)

    #convert 2d to 3d array, the model is only accept the 3d array to input
    _input_scaled3d = _input_scaled2d[:, :, numpy.newaxis]

    #make the prediction use saced model (the reconstructed_model)
    pred = reconstructed_model.predict(_input_scaled3d)
    pred = scaler.inverse_transform(pred)

    print("Prediction after inverse transform (micro mol/m2): ", pred)
    return pred