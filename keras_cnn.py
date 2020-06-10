# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 00:35:31 2020

@author: ojasr
"""
import tensorflow.keras as k
import numpy as np

def get_dataset(training=True):
    (train_images, train_labels), (test_images, test_labels) = k.datasets.fashion_mnist.load_data()
    if(training):
        train_images = np.expand_dims(train_images, axis=3);
        return (train_images, train_labels)
    else:
        test_images = np.expand_dims(test_images, axis=3);
        return (test_images, test_labels)

def build_model():
    model = k.Sequential([
            k.layers.Conv2D(64,kernel_size=3,activation='relu',input_shape=(28,28,1)),
            k.layers.Conv2D(32,kernel_size=3,activation='relu'),
            k.layers.Flatten(),
            k.layers.Dense(10,activation='softmax')
    ])
    
    model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])
    return model

def train_model(model, train_img, train_lab, test_img, test_lab, T):
    train_lab = k.utils.to_categorical(train_lab)
    test_lab =k.utils.to_categorical(test_lab)
    model.fit(train_img,train_lab,epochs = T,validation_data=(test_img,test_lab))

def predict_label(model, images, index): 
    p = model.predict(images)
    indP = p[index]
    
    class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
  
    si = np.argsort(indP)[::-1]
    
    
    for i in range(0,3):
        print("{}: {:.2f}%".format(class_names[si[i]],indP[si[i]]*100))

if __name__=="__main__":
    (tai,tal) = get_dataset()
    (tei,tel) = get_dataset(False)
    print(tai.shape)
    model = build_model()
    k.utils.plot_model(model,to_file='model.png')
    train_model(model, tai, tal, tei, tel, 5)
    predict_label(model,tei,0)
    