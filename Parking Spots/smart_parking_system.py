import cv2 as cv
import easyocr


def rotate(img, angle, rotPoint = None):
    (height, width) = img.shape[:2]
    if rotPoint is None:
        rotPoint = (width // 2, height // 2)

    rotMat = cv.getRotationMatrix2D(rotPoint, angle, 0.74)
    dimensions = (width, height)

    return cv.warpAffine(img, rotMat, dimensions)


def parking_spots(lst):
    lst2 = [0]*len(lst)
    for j in range(len(lst)):
        lst2[j] = lst[j][1]

    return lst2


imag = cv.imread('parking2.jpg')

reader = easyocr.Reader(['en'])

one_to_nine = parking_spots(reader.readtext(imag[0:180], mag_ratio=1.6))

rotated = rotate(imag, 90)
rotated_sliced1 = rotated[550:700, 500:700]
rotated_sliced2 = rotated[0:150, 500:700]

Th13_to_Th15 = parking_spots(reader.readtext(rotate(rotated_sliced1, 180)))

ten_to_twelve = parking_spots(reader.readtext(rotated_sliced2))

main_lst = one_to_nine + ten_to_twelve + Th13_to_Th15

f = open("parking_spots.txt", 'w')
for i in range(1, len(main_lst) + 2):
    if str(i) in main_lst:
        f.write(str("Spot " + str(i) + ': Free'))
        f.write('\n')
        # print("Spot", i, ': Free')
    else:
        f.write(str("Spot " + str(i) + ': Occupied'))
        f.write('\n')
        # print("Spot", i, ': Occupied')
f.close()

