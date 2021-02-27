from __future__ import print_function
import numpy as np
import time
import keras
from keras.utils import np_utils
from keras.models import Sequential, Model
from keras.layers import Dense, Activation, Convolution2D, MaxPooling1D, Flatten
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import Adam
from keras.optimizers import RMSprop
from keras.callbacks import ModelCheckpoint
from keras.applications import *
import random
from sklearn.model_selection import train_test_split

def load_data():

    labels = np.loadtxt('label.txt')
    encoded_seq = np.loadtxt('encoded_seq.txt')
    
    x_train,x_test,y_train,y_test = train_test_split(encoded_seq,labels,test_size=0.1)

    return np.array(x_train),np.array(y_train),np.array(x_test),np.array(y_test)


def cnn_classifier():

    model = Sequential()
        
    model.add(keras.layers.Conv1D(filters=50, kernel_size=9, strides=1, padding='same', batch_input_shape=(None, 400, 4), activation='relu'))    
    model.add(Dropout(0.3))

    
    model.add(Flatten())
    model.add(Dense(100,activation='relu'))
    
    model.add(Dense(3,activation='softmax'))
    
    adam = Adam(lr=1e-4)
    model.compile(optimizer=adam, loss='categorical_crossentropy', metrics=['accuracy'])

    return model


def training_process(x_train,y_train,x_test,y_test):
    
    x_train = x_train.reshape(-1, 400, 4)
    y_train = np_utils.to_categorical(y_train, num_classes=3)
    x_test = x_test.reshape(-1, 400, 4)
    y_true = y_test
    y_test = np_utils.to_categorical(y_test, num_classes=3)
    
    print("======================")
    print('Convolution Neural Network')
    start_time = time.time()
    model = cnn_classifier()
    model.fit(x_train, y_train, epochs=20, batch_size=50)
    model.save('CNN.h5')
    loss,accuracy = model.evaluate(x_test,y_test)
    print('testing accuracy: {}'.format(accuracy))
    print('training took %fs'%(time.time()-start_time))
    """
    predict = model.predict_classes(x_test).astype('int')
   
    true=[]
    wrong=[]
 
    for i in range(10000):
        if predict[i]!=y_true[i]:
            true.append(y_true[i])
            wrong.append(predict[i])
    print(len(true))
    print(len(wrong))
    
    zero_one=0
    zero_two=0
    one_zero=0
    one_two=0
    two_zero=0
    two_one=0

    for j in range(len(true)):
        if (true[j]==0 and wrong[j]==1):
            zero_one = zero_one+1
        elif (true[j]==0 and wrong[j]==2):
            zero_two = zero_two+1
        elif (true[j]==1 and wrong[j]==0):
            one_zero = one_zero+1
        elif (true[j]==1 and wrong[j]==2):
            one_two = one_two+1
        elif (true[j]==2 and wrong[j]==0):
            two_zero = two_zero+1
        elif (true[j]==2 and wrong[j]==1):
            two_one = two_one+1
    print('true:0,predict:1,%f'%zero_one)
    print('true:0,predict:2,%f'%zero_two)
    print('true:1,predict:0,%f'%one_zero)
    print('true:1,predict:2,%f'%one_two)
    print('true:2,predict:0,%f'%two_zero)
    print('true:2,predict:1,%f'%two_one)
    """



def main():
    x_train,y_train,x_test,y_test = load_data()
    
    training_process(x_train,y_train,x_test,y_test)



if __name__ == '__main__':
    main()
