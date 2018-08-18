from icrawler.builtin import GoogleImageCrawler
import os
import sys
import magic
import hashlib

directory = sys.argv[1]
label = sys.argv[2]
amt = sys.argv[3]

dir = directory + '/' + label
if not os.path.exists(dir):
	os.mkdir(dir)
google_crawler = GoogleImageCrawler(storage={'root_dir': dir}, downloader_threads=3, parser_threads=1)
google_crawler.crawl(keyword=label, offset=0, filters={'type': 'photo', 'date': ((2005, 1, 1), None)}, max_num=int(amt), min_size=(200,200), max_size=None)
print('Removing non jpg images')
for file in os.listdir(dir):
    file_type = magic.from_file(os.path.join(dir, file), mime=True)
    if file_type != 'image/jpeg':
        os.remove(os.path.join(dir, file))
        print(file + " was removed, is not a valid file format")
    else:
        with open(os.path.join(dir, file), 'rb') as f:
            shasum = hashlib.md5(f.read()).hexdigest()
            f.close()
            os.rename(os.path.join(dir, file), os.path.join(dir, shasum + '.jpg'))