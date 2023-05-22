import cv2 as cv
import easyocr

from split_image import split_image


def rotate(img, angle, rotpoint=None):
    (height, width) = img.shape[:2]
    if rotpoint is None:
        rotpoint = (width // 2, height // 2)

    rotmat = cv.getRotationMatrix2D(rotpoint, angle, 0.74)
    dimensions = (width, height)

    return cv.warpAffine(img, rotmat, dimensions)


def parking_spots(lst):
    lst2 = [0] * len(lst)
    for n in range(len(lst)):
        lst2[n] = lst[n][1]

    return lst2


spots = int(input('Please enter the number of spots the parking place has: '))
start_pt = int(input('Please enter the lowest spot number: '))

imag = cv.imread('parking_squared.jpg')

reader = easyocr.Reader(['en'])

check_list = []
check_list_temp = {}

exit_flag = False

for i in range(2, 6):
    if exit_flag:
        break

    for j in range(2, 6):
        if exit_flag:
            break

        check_list = []

        if i == j:
            sq_flag = True
        else:
            sq_flag = False

        split_image('parking_squared.jpg', i, j, sq_flag, False)

        for k in range(0, i + j):
            image = cv.imread(f'parking_squared_{k}.jpg')
            temp = parking_spots(reader.readtext(image, mag_ratio=1.6, allowlist='0123456789'))
            temp2 = parking_spots(reader.readtext(rotate(image, 90), mag_ratio=1.6, allowlist='0123456789'))
            temp3 = parking_spots(reader.readtext(rotate(image, 180), mag_ratio=1.6, allowlist='0123456789'))
            temp4 = parking_spots(reader.readtext(rotate(image, 270), mag_ratio=1.6, allowlist='0123456789'))

            temp = temp + temp2 + temp3 + temp4

            # print(temp)

            check_list += temp

        check_list = [int(x) for x in check_list if start_pt <= int(x) <= (spots + start_pt - 1)]
        check_list_temp = set(check_list)
        print(check_list_temp)

        if len(check_list_temp) == spots:
            check_list = sorted(list(check_list_temp))
            exit_flag = True
            print("width will be divided by: ", i)
            print("length will be divide by: ", j)
            print(check_list)
            print("Parking Place Calibrated Successfully")

        elif i == 5 and j == 5:
            print("Calibration Failed. Recapture Image")
