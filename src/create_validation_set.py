import os
import random
import shutil
import argparse

def progress_bar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    file = str(iteration) + '/' + str(total)
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%%|%s %s' % (prefix, bar, percent, file, suffix), end='\r')
    # Print New Line on Complete
    if iteration == total:
        print()

parser = argparse.ArgumentParser(description='Allows the creation a validation set with ease')
parser.add_argument('t_dir', metavar='Training Dir', type=str, nargs=1, help='Path to the training data set')
parser.add_argument('v_dir', metavar='Validation Dir', type=str, nargs=1, help='Path to the validation data set')
parser.add_argument('precent', metavar='Validation Precent', type=int, nargs=1, help='Precent of training images that will be copied to validation set')
args = parser.parse_args()

train_dir = vars(args)['t_dir'][0]
val_dir = vars(args)['v_dir'][0]
val_precent = vars(args)['precent'][0]

if not os.path.exists(train_dir):
    print('Path to train directory does not exist!')
    exit()

if not os.path.exists(val_dir):
    os.mkdir(val_dir)

for subdir in os.listdir(train_dir):
    val_amt = int(len(os.listdir(os.path.join(train_dir, subdir))) * float(int(val_precent) / 100))
    print('Copying %s random images from %s to %s' % (val_amt, os.path.join(train_dir, subdir), os.path.join(val_dir, subdir)))
    val_subdir_path = os.path.join(val_dir, subdir)
    if not os.path.exists(val_subdir_path):
        os.mkdir(val_subdir_path)
    else:
        response = input('%s validation class already exists, would you like to delete it and create a new one? yes or no: ' % subdir)
        if 'y' in response.lower():
            shutil.rmtree(val_subdir_path)
            os.mkdir(val_subdir_path)
            print('Done!')
        else:
            print('Not deleting %s validation class' % subdir)

    l = list(os.listdir(os.path.join(train_dir, subdir)))
    for iteration in range(val_amt):
        f = random.choice(list(enumerate(l)))
        index, file = f
        l.pop(index)
        shutil.copy2(os.path.join(train_dir, subdir, file), os.path.join(val_subdir_path, file))
        progress_bar(iteration + 1, val_amt, 'Progress')
print('Done!')