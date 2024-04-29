import tensorflow as tf
model = tf.keras.models.load_model('trained_model.h5')
# Compilar el modelo para construir las métricas
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
tf.saved_model.save(model, 'saved_model')
