import numpy as np
import matplotlib.pyplot as plt
from keras.src.layers import BatchNormalization
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import Callback, EarlyStopping, ModelCheckpoint
from sklearn.model_selection import train_test_split

# Load dataset as strings
x_special = np.load("x_special.npy")
y_special = np.load("y_special.npy")


# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(x_special, y_special, test_size=0.2, random_state=42)

# Determine input dimension from the data
input_dim = X_train.shape[1]

# Build the model
model = Sequential()
model.add(Dense(128, input_shape=(input_dim,), activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(1, activation='linear'))  # Changed to linear

model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])


history = model.fit(
    X_train, y_train,
    epochs=7,
    batch_size=32,
    validation_data=(X_test, y_test),
)

model.save("special_model2.keras")

# Predict using the model and plot histograms of predictions vs. actual values
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Model Loss During Training')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()


loss, mae = model.evaluate(X_test, y_test)
print(f"Loss: {loss}, MAE: {mae}")