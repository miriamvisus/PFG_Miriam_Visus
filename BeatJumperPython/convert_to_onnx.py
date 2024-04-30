import tf2onnx.convert
import onnx
from tensorflow.keras.models import load_model

model = load_model('trained_model.h5')

onnx_model = tf2onnx.convert.from_keras(model)
onnx.save(onnx_model, 'trained_model.onnx')
