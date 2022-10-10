# importing the required libraries
import cv2
import os
import PIL.Image as Image

# importing the helper__functions
from helper_functions import read_pascal, compute_iou

# module to load dataset into 2 categories : plate and not_plate
def load_dataset():
    # specifying path for given folders where images have to be saved
    car_save_path = 'use_data/plate/'
    no_car_save_path = 'use_data/not_plate/'

    # initialising the count variable to 0
    total_not_car = 0
    total_car = 0

    # iterating over each file using for loop
    for file in os.listdir('data/'):

        # if file is .png file
        if '.png' in file:

            # find the xml file for it
            # read_pascal module provides xmin, ymin, xmax, ymax (co ordinates of bounding box) values with filename
            name, box_list = read_pascal('data/' + file.split('.')[0] + '.xml')

            # using selective search algorithm provided by opencv
            # find different regions based on similarity of color, texture
            ss = cv2.ximgproc.segmentation.createSelectiveSearchSegmentation()
            pic = cv2.imread('data/' + file)
            pic_copy = pic.copy()

            ss.setBaseImage(pic)
            ss.switchToSelectiveSearchFast()
            results = ss.process()

            car_count = 0
            no_car_count = 0
            total_counted = 0
            for found_box in results:
                # in form of x, y, w, h
                found_box_use = [found_box[0], found_box[1], found_box[0] + found_box[2], found_box[1] + found_box[3]]
                image_roi = pic_copy[found_box[1]:found_box[3] + found_box[1], found_box[0]:found_box[0] + found_box[2]]

                # compute_iou checks if the region matches to region of ground-truth bounding box
                iou = compute_iou(found_box_use, box_list[0])  # its a nested list, so we take the 1st element
                print(iou)
                print('THERE')

                # if iou > 0.7, save image in plate folder
                if iou > 0.7:
                    if car_count < 16:  # don't have enough memory for too many

                        image_roi_use = cv2.resize(image_roi, (128, 128))
                        image_roi_use = Image.fromarray(image_roi_use)
                        image_roi_use.save(car_save_path + 'plate_' + str(total_car) + '.png')

                        total_car += 1
                        car_count += 1

                # if iou < 0.3, save image in not_plate folder
                if iou < 0.3:
                    if no_car_count < 16:
                        image_roi_use = cv2.resize(image_roi, (128, 128))
                        image_roi_use = Image.fromarray(image_roi_use)
                        image_roi_use.save(no_car_save_path + 'not_plate_' + str(total_not_car) + '.png')
                        total_not_car += 1
                        no_car_count += 1

                if total_counted > 999:
                    break

                total_counted += 1

# make the function call
print('Start loading...')
load_dataset()
print("Loaded Successfully")
