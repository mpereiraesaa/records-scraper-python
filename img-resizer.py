from PIL import Image
import os

def resize_multiple_images(src_path):
    for filename in os.listdir(src_path):
        try:
            img=Image.open(src_path + "/" + filename)
            new_img = img.resize((89,30))
            new_img.save(src_path + "/" + filename)
            print('Resized and saved {} successfully.'.format(filename))
        except:
            continue

src_path = os.getcwd() + "/dataset/training"
resize_multiple_images(src_path)
