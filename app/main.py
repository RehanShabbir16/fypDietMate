import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import pandas as pd

import io
import tensorflow as tf
from tensorflow import keras
from PIL import Image
import base64

from flask import Flask, request, jsonify

model = keras.models.load_model("food101.h5")
def transform_image(filename, img_shape=224, scale=True):
  """
  Reads in an image from filename, turns it into a tensor and reshapes into
  (224, 224, 3).

  Parameters
  ----------
  filename (str): string filename of target image
  img_shape (int): size to resize target image to, default 224
  scale (bool): whether to scale pixel values to range(0, 1), default True
  """
  # Read in the image
  img=tf.convert_to_tensor(filename)
  # img = tf.io.read_file(filename)
  # # Decode it into a tensor
  # img = tf.io.decode_image(img)
  img = tf.image.resize(img, [img_shape, img_shape])
  if scale:
    # Rescale the image (get all values between 0 and 1)
    return img/255.
  else:
    return img
    
def predicts(img):

        # Transform the image as required by your model
  img_tf = transform_image(img, scale=False)

        # Make the prediction
  pred_prob = model.predict(tf.expand_dims(img_tf, axis=0)) # make prediction on image with shape [None, 224, 224, 3]
  pred_class = classes_names[pred_prob.argmax()]
  print(pred_class)# find the predicted class 

  df = pd.read_csv('nutri.csv')

    # Check that the CSV file was read correctly
  if df.empty:
    return "Error: CSV file is empty"

    # Search for the food name in the DataFrame
  result = df[df['Food'] == pred_class]

    # Check that the food name was found in the DataFrame
  if result.empty:
      return f"Food '{result}' not found in the dataset."

    # Extract the attributes (replace 'Protein', 'Carbs', 'Calories' with actual column names)
  protein = result['Protein'].values[0]
  carbs = result['Carbs'].values[0]
  calories = result['Calories'].values[0]
  return f"Food: {pred_class}",f" Protein: {protein}",f" Carbs: {carbs}",f" Calories: {calories}"

classes_names= [
    "Apple Pie", "Baby Back Ribs", "Burger", "Beef Carpaccio", "Beef Tartare",
    "Beet Salad", "Beignets", "Bibimbap", "Bread Pudding", "Breakfast Burrito",
    "Bruschetta", "Caesar Salad", "Cannoli", "Caprese Salad", "Carrot Cake",
    "Ceviche", "Cheese Plate", "Cheesecake", "Chicken Curry", "Chicken Quesadilla",
    "Chicken Wings", "Chocolate Cake", "Chocolate Mousse", "Churros", "Clam Chowder",
    "Club Sandwich", "Crab Cakes", "Creme Brulee", "Croque Madame", "Cupcakes",
    "Deviled Eggs", "Donuts", "Dumplings", "Edamame", "Eggs Benedict",
    "Escargots", "Falafel", "Filet Mignon", "Fish and Chips", "Foie Gras",
    "French Fries", "French Onion Soup", "French Toast", "Fried Calamari", "Fried Rice",
    "Frozen Yogurt", "Garlic Bread", "Gnocchi", "Greek Salad", "Grilled Cheese Sandwich",
    "Grilled Salmon", "Guacamole", "Gyoza", "Hamburger", "Hot and Sour Soup",
    "Hot Dog", "Huevos Rancheros", "Hummus", "Ice Cream", "Lasagna", "Lobster Bisque",
    "Lobster Roll Sandwich", "Macaroni and Cheese", "Macarons", "Miso Soup", "Mussels",
    "Nachos", "Omelette", "Onion Rings", "Oysters", "Pad Thai", "Paella", "Pancakes",
    "Panna Cotta", "Peking Duck", "Pho", "Pizza", "Pork Chop", "Poutine", "Prime Rib",
    "Pulled Pork Sandwich", "Ramen", "Ravioli", "Red Velvet Cake", "Risotto", "Samosa",
    "Sashimi", "Scallops", "Seaweed Salad", "Shrimp and Grits", "Spaghetti Bolognese",
    "Spaghetti Carbonara", "Spring Rolls", "Steak", "Strawberry Shortcake", "Sushi",
    "Tacos", "Takoyaki", "Tiramisu", "Tuna Tartare", "Waffles"
]



# a=predicts('sushi.jpg')
# print(a)

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get('file')
        if file is None or file.filename == "":
            return jsonify({"error": "no file"})

        try:
          
          image_bytes = file.read()
          pillow_img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
          # Convert PIL Image to NumPy array

          label0= predicts(pillow_img)
          data = {label0}
          print(data)
          return jsonify(data)
        
        except Exception as e:
            return jsonify({"error": str(e)})




    return "OK"


if __name__ == "__main__":
    app.run(debug=True)
    

