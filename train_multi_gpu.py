import argparse
import os
from time import time
import sklearn


def main():
    parser = argparse.ArgumentParser(description='Train the model with training data')
    parser.add_argument('root_dir', metavar='path', type=str, nargs=1, help='Root data folder where the test and validation sets are')
    parser.add_argument('gpus', type=int, nargs=1, help='Amout of gpus to use')
    parser.add_argument('epochs', metavar='epochs', type=int, nargs=1, help='How many epochs the training will consist of')
    args = parser.parse_args()
    root_dir = vars(args)['root_dir'][0]
    epochs = vars(args)['epochs'][0]
    gpus = vars(args)['gpus'][0]
    print(root_dir)

    import keras
    model = keras.utils.multi_gpu_model(keras.models.Sequential(), gpus=int(gpus))

    model.add(keras.layers.Conv2D(32, (3, 3), input_shape=(100, 100, 3)))
    model.add(keras.layers.Activation('relu'))
    model.add(keras.layers.MaxPooling2D(pool_size=(2, 2)))

    model.add(keras.layers.Conv2D(32, (3, 3), border_mode='same'))
    model.add(keras.layers.Activation('relu'))
    model.add(keras.layers.MaxPooling2D(pool_size=(2, 2)))

    model.add(keras.layers.Conv2D(64, (3, 3), border_mode='same'))
    model.add(keras.layers.Activation('relu'))
    model.add(keras.layers.MaxPooling2D(pool_size=(2, 2)))

    model.add(keras.layers.Flatten())
    model.add(keras.layers.Dense(64))
    model.add(keras.layers.Activation('relu'))
    model.add(keras.layers.Dropout(0.5))
    model.add(keras.layers.Dense(5))
    model.add(keras.layers.Activation('sigmoid'))

    sgd = keras.optimizers.SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

    train_datagen = keras.preprocessing.image.ImageDataGenerator(
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True)

    val_datagen = keras.preprocessing.image.ImageDataGenerator(rescale=1./255)
    train_data = train_datagen.flow_from_directory(os.path.join(root_dir, 'train'), target_size=(100, 100))
    train_img_count = 0
    for sub in os.listdir(os.path.join(root_dir, 'train')):
        amt = os.listdir(os.path.join(root_dir, 'train', sub))
        train_img_count = train_img_count + len(amt)
    val_data = val_datagen.flow_from_directory(os.path.join(root_dir, 'validation'), target_size=(100, 100))
    val_img_count = 0
    for sub in os.listdir(os.path.join(root_dir, 'validation')):
        amt = os.listdir(os.path.join(root_dir, 'validation', sub))
        val_img_count = val_img_count + len(amt)
    tensorboard = keras.callbacks.TensorBoard(log_dir='logs/{}'.format(time()))

    model.fit_generator(train_data, steps_per_epoch=train_img_count // 32, epochs=epochs, validation_data=val_data, validation_steps=val_img_count // 32, callbacks=[tensorboard])
    model.save('model')

if __name__ == '__main__':
    main()