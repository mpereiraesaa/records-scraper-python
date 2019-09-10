from PIL import Image
import os

def rename_multiple_images(src_path):
    i = 0
    for filename in os.listdir(src_path):
        i += 1
        try:
            dst = src_path + "/" + str(i) + ".png"
            src = src_path + "/" + filename
            os.rename(src, dst)
            print('Renamed successfully.'.format(filename))
        except:
            continue

src_path = os.getcwd() + "/dataset/training"
rename_multiple_images(src_path)
