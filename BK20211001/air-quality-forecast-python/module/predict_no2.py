from tensorflow import keras
from pickle import load
import numpy
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))


def predict_from_val(input=0):
    # load the model
    reconstructed_model = keras.models.load_model(dir_path+ '/models-py/rnn-lstm-no2', custom_objects=None, compile=True, options=None)

    # load the scaler: with fit_transformed by the dataset
    scaler = load(open(dir_path+ '/models-py/rnn-lstm-no2/scaler.pkl', 'rb'))

    _input2d = numpy.array([[input]])

    #transform input by saved scaler
    _input_scaled2d = scaler.transform(_input2d)

    #convert 2d to 3d array, the model is only accept the 3d array to input
    _input_scaled3d = _input_scaled2d[:, :, numpy.newaxis]
    #print(_input_scaled3d)

    #make the prediction use saced model (the reconstructed_model)
    pred = reconstructed_model.predict(_input_scaled3d)
    pred = scaler.inverse_transform(pred)

    print("Prediction after inverse transform (micro mol/m2): ", pred)
    return pred


# a = predict_from_val(0.01)

# print("aaaaaaaaaa", a)