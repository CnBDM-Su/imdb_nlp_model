from tensorflow.keras.datasets import imdb
from tensorflow.keras.preprocessing import sequence
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout

#initial data
vocabulary_size = 5000
(x_train,y_train), (x_test,y_test)=imdb.load_data(num_words= vocabulary_size)
print('loaded dataset with {} training samples, {} test samples'.format(len(x_train), len(x_test)))
max_words = 500
x_train = sequence.pad_sequences(x_train,maxlen=max_words)
x_test = sequence.pad_sequences(x_test,maxlen=max_words)

#build model
embedding_size = 32
model = Sequential()
model.add(Embedding(vocabulary_size, embedding_size, input_length=max_words))
model.add(LSTM(100))
model.add(Dense(1, activation='sigmoid'))
print(model.summary())

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

#train model
batch_size = 64
num_epochs = 3
x_valid, y_valid= x_train[:batch_size],y_train[:batch_size]
x_train2, y_train2= x_train[batch_size:],y_train[batch_size:]
model.fit(x_train2,y_train2, validation_data=(x_valid,y_valid), batch_size=batch_size, epochs=num_epochs)

#evaluate
scores = model.evaluate(x_test, y_test, verbose=0)
print('TA:', scores[1])
