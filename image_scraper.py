from icrawler.builtin import GoogleImageCrawler
import os
import magic
import hashlib
import argparse

parser = argparse.ArgumentParser(description="scrape the internet for training images")
parser.add_argument('dir', metavar='Directory', type=str, nargs=1, help='Path to the testing data')
parser.add_argument('label', metavar='Label', type=str, nargs=1, help='The name of the images to download')
parser.add_argument('amt', metavar='Download Amount', type=int, nargs=1, help='The maximum amount of images to download')
args = parser.parse_args()
directory = vars(args)['dir'][0]
label = vars(args)['label'][0]
amt = vars(args)['amt'][0]

dir = os.path.join(directory, label)
if not os.path.exists(dir):
    os.mkdir(dir)
google_crawler = GoogleImageCrawler(storage={'root_dir': dir}, downloader_threads=3, parser_threads=1)
google_crawler.crawl(keyword=label, offset=0, filters={'type': 'photo', 'date': ((2005, 1, 1), None)}, max_num=int(amt),
                     min_size=(200, 200), max_size=None)
print('Removing non valid image files')
for file in os.listdir(dir):
    file_type = magic.from_file(os.path.join(dir, file), mime=True)
    if (file_type != 'image/jpeg') or (file_type != 'image/png'):
        os.remove(os.path.join(dir, file))
        print(file + " was removed, is not a valid file format")
    else:
        with open(os.path.join(dir, file), 'rb') as f:
            shasum = hashlib.md5(f.read()).hexdigest()
            f.close()
            os.rename(os.path.join(dir, file), os.path.join(dir, shasum + '.jpg'))