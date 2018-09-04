import keras
import sys
import os

def main():
    model = keras.models.Sequential()

    model.add(keras.layers.Conv2D(32, (3, 3), input_shape=(100, 100, 3)))
    model.add(keras.layers.Activation('relu'))
    model.add(keras.layers.MaxPooling2D(pool_size=(2, 2)))

    model.add(keras.layers.Conv2D(32, (3, 3)))
    model.add(keras.layers.Activation('relu'))
    model.add(keras.layers.MaxPooling2D(pool_size=(2, 2)))

    model.add(keras.layers.Conv2D(64, (3, 3)))
    model.add(keras.layers.Activation('relu'))
    model.add(keras.layers.MaxPooling2D(pool_size=(2, 2)))

    model.add(keras.layers.Flatten())
    model.add(keras.layers.Dense(64))
    model.add(keras.layers.Activation('relu'))
    model.add(keras.layers.Dropout(0.5))
    model.add(keras.layers.Dense(1))
    model.add(keras.layers.Activation('sigmoid'))

    model.compile(loss='binary_crossentropy', optimizer='Adam', metrics=['accuracy'])


    train_datagen = keras.preprocessing.image.ImageDataGenerator(
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True)

    val_datagen = keras.preprocessing.image.ImageDataGenerator(rescale=1./255)
    root_data = sys.argv[1]
    train_data = train_datagen.flow_from_directory(os.path.join(root_data, 'train'), target_size=(100, 100), class_mode="binary")
    train_img_count = 0
    for sub in os.listdir(os.path.join(root_data, 'train')):
        amt = os.listdir(os.path.join(root_data, 'train', sub))
        train_img_count = train_img_count + len(amt)
    val_data = val_datagen.flow_from_directory(os.path.join(root_data, 'validation'), target_size=(100, 100), class_mode="binary")
    val_img_count = 0
    for sub in os.listdir(os.path.join(root_data, 'validation')):
        amt = os.listdir(os.path.join(root_data, 'validation', sub))
        val_img_count = val_img_count + len(amt)
    tensorboard = keras.callbacks.TensorBoard(log_dir='logs')

    model.fit_generator(train_data, steps_per_epoch=train_img_count // 32, epochs=sys.argv[2], validation_data=val_data, validation_steps=val_img_count // 32, callbacks=[tensorboard])
    model.save_weights('weights.h5')
main()