import os

# specify the img directory path
path = "/Users/julia/PycharmProjects/PPE_Detection_Yolov8/PPE_Images/"

# list files in img directory
files = os.listdir(path)

for file in files:
    # make sure file is an image
    if file.endswith(('.jpg', 'jpeg')):
        img_path = path + file

image_strings = [path + str(p) for p in files]
print(image_strings)