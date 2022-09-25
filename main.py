import random
import time
import sqlite3

import numpy as np

import tensorflow as tf

from flask import Flask, render_template, request, url_for, flash, redirect
from flask_bootstrap import Bootstrap

# ...
app = Flask(__name__)
app.config['SECRET_KEY'] = 'lkerm234945mkewmfkmerfkjerng'
bootstrap = Bootstrap(app)
db_file = 'herbClassifier.db'


def classifyHerb(img_file):
    print("Image: ", img_file)
    new_model = tf.keras.models.load_model('models/saved_model')

    img_height = 180
    img_width = 180

    img_file = tf.keras.utils.load_img(
        img_file, target_size=(img_height, img_width)
    )
    img_array = tf.keras.utils.img_to_array(img_file)
    img_array = tf.expand_dims(img_array, 0)  # Create a batch

    predictions = new_model.predict(img_array)
    score = tf.nn.softmax(predictions[0])
    class_names = ['daisy', 'dandelion', 'roses', 'sunflowers', 'tulips']
    print(
        "This image most likely belongs to {} with a {:.2f} percent confidence."
        .format(class_names[np.argmax(score)], 100 * np.max(score))
    )
    anc = class_names[np.argmax(score)]
    return class_names[np.argmax(score)], 100 * np.max(score)


def check_edibility(plant_name):
    edibility = None
    conn = sqlite3.connect(db_file)
    cursor = conn.execute("SELECT edible from herbList where herbPrimaryName like '%" + plant_name + "%'")
    edibility = cursor.fetchall()[0][0]
    conn.close()
    print(edibility)
    return edibility


def check_description(plant_name):
    description = None
    conn = sqlite3.connect(db_file)
    cursor = conn.execute("SELECT herbDescription from herbList where herbPrimaryName like '%" + plant_name + "%'")
    description = cursor.fetchall()[0][0]
    conn.close()
    print(description)
    return description


def check_herb_other_names(plant_name):
    description = None
    conn = sqlite3.connect(db_file)
    cursor = conn.execute("SELECT herbOtherNames from herbList where herbPrimaryName like '%" + plant_name + "%'")
    description = cursor.fetchall()[0][0]
    conn.close()
    print(description)
    return description

def check_recipie(plant_name):
    description = None
    conn = sqlite3.connect(db_file)
    cursor = conn.execute("SELECT recipie from herbList where herbPrimaryName like '%" + plant_name + "%'")
    description = cursor.fetchall()[0][0]
    conn.close()
    print(description)
    return description

def check_link(plant_name):
    description = None
    conn = sqlite3.connect(db_file)
    cursor = conn.execute("SELECT source from herbList where herbPrimaryName like '%" + plant_name + "%'")
    description = cursor.fetchall()[0][0]
    conn.close()
    print(description)
    return description

def check_antidote(plant_name):
    description = None
    conn = sqlite3.connect(db_file)
    cursor = conn.execute("SELECT Antidote from herbList where herbPrimaryName like '%" + plant_name + "%'")
    description = cursor.fetchall()[0][0]
    conn.close()
    print(description)
    return description

@app.route('/', methods=('GET', 'POST'))
def homePage():
    if request.method == 'POST':
        file_objectUpload = request.files['file']
        file_objectCapture = request.files['fileCapture']
        fileObject = file_objectUpload
        if len(file_objectCapture.filename) > len(file_objectUpload.filename):
            fileObject = file_objectCapture
        filename = 'static/assets/' + str(int(time.time())) + fileObject.filename

        if fileObject.filename != '':
            fileObject.save(filename)
            plant_name, score = classifyHerb(filename)
            if score < 90:
                is_edible = 'Unknown'
                plant_description = 'Not yet classified'

            else:
                is_edible = check_edibility(plant_name)
                plant_description = check_description(plant_name)
                herbOtherName = check_herb_other_names(plant_name)
                linktoHerb = check_link(plant_name)
                herbRecipie = check_recipie(plant_name)
                herbAntidote = check_antidote(plant_name)
            return render_template('result.html', filepath=filename,
                                   verdict=is_edible, description=plant_description,recepie=herbRecipie,
                                   herbName = plant_name, othername=herbOtherName, herbLink=linktoHerb,
                                   antidote = herbAntidote)
    return render_template('index.html')


@app.route('/result')
def showEdibility():
    return '<h1>Hello, World!</h1>'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
