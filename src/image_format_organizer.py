import os
import magic
import argparse

parser = argparse.ArgumentParser(description="scrape the internet for training images")
parser.add_argument('dir', type=str, nargs=1, help='Path to the testing data')
args = vars(parser.parse_args())
directory = args['dir'][0]

for sub_dir in os.listdir(directory):
    for sub_sub_dir in os.listdir(os.path.join(directory, sub_dir)):
        for file in os.listdir(os.path.join(directory, sub_dir, sub_sub_dir)):
            file_path = os.path.join(directory, sub_dir, sub_sub_dir, file)
            file_type = magic.from_file(file_path, mime=True)
            if file_type == 'image/jpeg':
                name = file.split('.')[0]
                ext = file.split('.')[1]
                if ext == 'jpg':
                    pass
                else:
                    new_path = os.path.join(directory, sub_dir, sub_sub_dir, name) + '.jpg'
                    os.rename(file_path, new_path)
            elif file_type == 'image/png':
                name = file.split('.')[0]
                ext = file.split('.')[1]
                if ext == 'png':
                    pass
                else:
                    new_path = os.path.join(directory, sub_dir, sub_sub_dir, name) + '.png'
                    os.rename(file_path, new_path)