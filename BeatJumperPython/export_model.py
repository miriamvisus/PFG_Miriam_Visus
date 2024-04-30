import tensorflow as tf

model = tf.keras.models.load_model('trained_model.h5')
# Export the model
tf.saved_model.save(model, "saved_model")
# python -m tf2onnx.convert --saved-model ./saved_model --output trained_model.onnx