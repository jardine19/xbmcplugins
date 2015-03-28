#!/usr/bin/env python
import os
import zipfile

def zipdir(path, zip):
    for root, dirs, files in os.walk(path):
        for file in files:
            if ".zip" not in file:
                zip.write(os.path.join(root, file))

if __name__ == '__main__':
    zipf = zipfile.ZipFile('Python.zip', 'w')
    zipdir('plugin.video.eetv', zipf)
    zipf.close()