from PIL import Image
import os

image_path = os.getcwd() + "/dataset/test"

sizeW = 89
sizeH = 30

def divide_in_blocks(src_image):
    img = Image.open(src_image)
    width, height = img.size

    for x0 in range(0, width, sizeW):
        for y0 in range(0, height, sizeH):
            xSize = x0 + sizeW
            ySize = y0 + sizeH
            if (xSize < width and ySize < height):
                box = (x0, y0, xSize, ySize)
                print("%s %s" % (src_image, box))
                img.crop(box).save('%s.crop.x%03d.y%03d.jpg' % (src_image.replace('.jpg', ''), x0, y0))

for filename in os.listdir(image_path):
    try:
        divide_in_blocks(image_path + "/" + filename)
    except:
        continue
