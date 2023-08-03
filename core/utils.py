from tensorflow.keras.preprocessing import image
import numpy as np

def predict_fire(image_path, model):
    img = image.load_img(image_path, target_size=(300, 300))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    classes = model.predict(x)
    if classes[0][0] > 0.5:
        return "not fire"
    else:
        return "fire"
