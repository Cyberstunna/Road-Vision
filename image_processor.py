import pytesseract 
import matplotlib.pyplot as plt
import cv2
import glob
import os

class ReadLicensePlate:

    def check_image(self, image):
        list_license_plates = []
        predicted_license_plates = []

        list_license_plates.append(image)

        image = cv2.imread(list_license_plates[0])

        resize_image = cv2.resize(image, None, fx = 2, fy = 2, interpolation = cv2.INTER_CUBIC)

        grayscale_resize_image = cv2.cvtColor(resize_image, cv2.COLOR_BGR2GRAY)

        gaussian_blur_image = cv2.GaussianBlur(grayscale_resize_image, (5, 5), 0)

        predicted_result = pytesseract.image_to_string(gaussian_blur_image, lang ='eng', config ='--oem 3 -l eng --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')

        filter_predicted_result = "".join(predicted_result.split()).replace(":", "").replace("-", "")

        print(filter_predicted_result)
        
        predicted_license_plates.append(filter_predicted_result)

        #self.calculate_predicted_accuracy(list_license_plates, predicted_license_plates)
        return predicted_license_plates

    def calculate_predicted_accuracy(self, actual_list, predicted_list):
        for actual_plate, predict_plate in zip(actual_list, predicted_list):
            accuracy = "0 %"
            num_matches = 0
            if actual_plate == predict_plate:
                accuracy = "100 %"
            else:
                if len(actual_plate) == len(predict_plate):
                    for a, p in zip(actual_plate, predict_plate):
                        if a == p: 
                            num_matches += 1
                    accuracy = str(round((num_matches / len(actual_plate)), 2) * 100)
                    accuracy += "%"
            print("     ", actual_plate, "\t\t\t", predict_plate, "\t\t  ", accuracy)