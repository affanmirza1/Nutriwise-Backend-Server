## Function

def predict_image(fruit_img_path):
    
    # load model
    import tensorflow as tf
    model = tf.keras.models.load_model('Model.h5')
    
    # defining labels
    labels = ['apple','banana', 'beetroot', 'bell pepper', 'cabbage', 'capsicum', 'carrot', 'cauliflower', 'chilli pepper', 'corn', 'cucumber', 'eggplant', 'garlic', 'ginger', 'grapes', 'jalapeno', 'kiwi', 'lemon', 'lettuce', 'mango', 'onion', 'orange', 'paparika', 'pear', 'peas', 'pineapple', 'pomegranate', 'potato', 'raddish', 'soy beans', 'spinach', 'sweetcorn', 'sweetpotato', 'tomato', 'turnip', 'watermelon']
    
    #preprocess image
    from tensorflow.keras.preprocessing import image
    import numpy as np
    img = image.load_img(fruit_img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)
    
    # make prediction
    prediction_array = model.predict(img_array)
    predicted_class_index = np.argmax(prediction_array)
    prediction = labels[predicted_class_index]
    
    # return fruit_name prediction
    return prediction