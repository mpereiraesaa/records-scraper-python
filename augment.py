import Augmentor
import os

image_path = os.getcwd() + "/dataset/training"

p = Augmentor.Pipeline(image_path)

# p.rotate(probability=0.7, max_left_rotation=10, max_right_rotation=10)
# p.zoom(probability=0.5, min_factor=0.5, max_factor=1.5)
# p.zoom_random(probability=0.5, percentage_area=0.8)
# p.flip_left_right(probability=0.5)
# p.flip_top_bottom(probability=0.5)
# p.random_distortion(probability=1, grid_width=4, grid_height=4, magnitude=8)
# p.crop_random(probability=1, percentage_area=0.5)
# p.random_brightness(probability=0.7, min_factor= 0.5, max_factor=1.5)
p.random_contrast(probability=0.7, min_factor= 0.5, max_factor=1.5)

p.sample(100)
