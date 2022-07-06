import tensorflow as tf
import numpy as np
import cv2
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam

def make_model():
    train=ImageDataGenerator(rescale=1/255)
    validation=ImageDataGenerator(rescale=1/255)

    train_dataset=train.flow_from_directory('Dataset/Training/',target_size=(224,224),
                                        class_mode='categorical',shuffle=True)
    validation_dataset=validation.flow_from_directory('Dataset/validation/',target_size=(224,224)
                                        ,class_mode='categorical',shuffle=True)


    model=tf.keras.models.Sequential([tf.keras.layers.Conv2D(16,(3,3),activation='relu',input_shape=(224,224,3)),
                                    tf.keras.layers.MaxPool2D(2,2),
                                    tf.keras.layers.Conv2D(32,(3,3),activation='relu',input_shape=(224,224,3)),
                                    tf.keras.layers.MaxPool2D(2,2),
                                    tf.keras.layers.Conv2D(64,(3,3),activation='relu',input_shape=(224,224,3)),
                                    tf.keras.layers.MaxPool2D(2,2),
                                    tf.keras.layers.Flatten(),
                                    tf.keras.layers.Dense(512,activation='relu'),
                                    tf.keras.layers.Dense(3,activation='softmax')])

    model.compile(loss='categorical_crossentropy',
                    optimizer=Adam(lr=0.0001),
                    metrics=['acc'])

    history= model.fit(train_dataset,
                        steps_per_epoch = 15,
                        epochs =100,
                        validation_data = validation_dataset,
                        validation_steps = 15)

    score = model.evaluate(validation_dataset)
    print('Test accuracy:', score[1])

    model.save("Smoke_and_Fire_Classifier.h5")

if __name__ == "__main__" :
    make_model()