import cv2
from keras import Model,Sequential
import keras.layers as l
import csv
import numpy as np
from random import sample
from keras.optimizers import Adam

# Data preprocessing
for i in range(2,10):
    vidcap = cv2.VideoCapture("output"+str(i)+".avi")
    print("preparing data")
    success = True
    images = []
    while success:
        success, image = vidcap.read()
        if success:
            # print(image)
            image = cv2.resize(image,(80,60))
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            image = np.expand_dims(image,2)
            print(image.shape)
            image = np.true_divide(image,255)
            images.append(image)
    steering = []
    with open("output"+str(i)+".csv") as steer:
        reader = csv.reader(steer,delimiter=",")
        count = 0
        for row in reader:
            if not count == 0:
                steering.append(int(row[2]))
            count+=1
images = np.asarray(images)
steering = np.asarray(steering)
# ids = []
# for i in range(5570):
#     ids.append(i)
# traini = sample(ids,4000)
# vali = []
# for i in ids:
#     if not i in traini:
#         vali.append(i)
# trainx = []
# trainy = []
# valx = []
# valy = []
# for i in traini:
#     trainx.append(images[i])
#     trainy.append(steering[i])
# for i in vali:
#     valx.append(images[i])
#     valy.append(steering[i])
# trainx = np.asarray(trainx)
# trainy = np.asarray(trainy)
# valx = np.asarray(valx)
# valy = np.asarray(valy)

#Neural Network Setup
batch_size = 2
dropout = .4
model = Sequential()
model.add(l.Conv2D(256,activation="relu",kernel_size=(3,3),input_shape=(60,80,1),data_format="channels_last"))
model.add(l.Conv2D(128,activation="relu",kernel_size=(3,3),data_format="channels_last"))
model.add(l.Conv2D(64,activation="relu",kernel_size=(3,3),data_format="channels_last"))
model.add(l.Flatten())
model.add(l.Dense(100,activation="relu"))
model.add(l.Dropout(dropout))
model.add(l.BatchNormalization())
model.add(l.Dense(50,activation="relu"))
model.add(l.Dropout(dropout))
model.add(l.BatchNormalization())
model.add(l.Dense(1,activation="relu"))
model.compile(optimizer=Adam(),loss="mean_squared_logarithmic_error")

#Neural Network Training
print("starting training")
model.fit(images,steering,batch_size=batch_size,epochs=10,validation_split=.3)
model.save("checkpoint/model_0.h5")

