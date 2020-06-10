# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 13:01:49 2020

@author: ojasr
"""
import tensorflow.keras as k
import matplotlib.pyplot as mp
import numpy as np

def get_dataset(training=True):
    (train_images, train_labels), (test_images, test_labels) = k.datasets.fashion_mnist.load_data()
    if(training):
        return (train_images,train_labels)
    else:
        return (test_images, test_labels)
    
def print_stats(images, labels):
    print(labels.size)
    imX = len(images[0])
    imY = len(images[0][0])
    print(imX,"x",imY)
    
    class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
    cVal = [0,0,0,0,0,0,0,0,0,0]
    for l in labels:
        cVal[l] += 1
    
    
    for i in range(0,10):
        print(class_names[i],"-",cVal[i])
        
def view_image(image, label):
    #subplots
    fig, (original) = mp.subplots(1)
    original.set_title('Original')
    imageShow = original.imshow(image,aspect='equal')
    fig.colorbar(imageShow, ax=original)
    
    #render
    mp.show()
    
def build_model():
    model = k.Sequential([
      k.layers.Flatten(input_shape=(28,28)),
      k.layers.Dense(128,activation='relu'),
      k.layers.Dense(10)
    ])
    
    model.compile(loss=k.losses.SparseCategoricalCrossentropy(from_logits=True),optimizer='adam',metrics=['accuracy'])
    return model

def train_model(model, images, labels, T):
    model.fit(images,labels, None, epochs = T)
    
def evaluate_model(model, images, labels, show_loss=True):
    tl,ta = model.evaluate(images,labels,verbose=False)
    ta*=100
    
    print("Accuracy: {:.2f}%".format(ta))
    if(show_loss):
        print("Loss: {:.2f}".format(tl))

def predict_label(model, images, index):
    model.add(k.layers.Softmax())
    p = model.predict(images)
    indP = p[index]
    
    class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
  
    si = np.argsort(indP)[::-1]
    
    
    for i in range(0,3):
        print("{}: {:.2f}%".format(class_names[si[i]],indP[si[i]]*100))

"""
if __name__=="__main__":
    ti,tl = get_dataset()
    type(ti)
    print_stats(ti,tl)
    model = build_model()
    train_model(model,ti,tl,5)
    evaluate_model(model,ti,tl)
    predict_label(model,ti,0)
"""
