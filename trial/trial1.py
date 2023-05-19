import cv2
import easyocr




import arabic_reshaper 
from bidi.algorithm import get_display
import numpy as np
from PIL import ImageFont, ImageDraw, Image


# load the image and resize it
def AI(frame,resize):
    #image = cv2.imread(frame)
    #image = cv2.resize(image, (800, 600))
    #image = cv2.resize(frame, (800, 600))
    image = frame
    if(resize):
        image = cv2.resize(frame, (800, 600))

    # convert the input image to grayscale,
    # blur it, and detect the edges 
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
    blur = cv2.GaussianBlur(gray, (5,5), 0) 
    edged = cv2.Canny(blur, 10, 200) 
    # cv2.imshow('Canny', edged)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # find the contours, sort them, and keep only the 5 largest ones
    contours, _ = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = cv2.contourArea, reverse = True)[:5]
    approx = []
    # loop over the contours
    for c in contours:
        # approximate each contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.08 * peri, True)
        # if the contour has 4 points, we can say
        # that we have found our license plate
        #print(approx)
        if len(approx) == 4:
            n_plate_cnt = approx
            break        
    if(len(approx) !=4):
        return
    # get the bounding box of the contour and 
    # extract the license plate from the image
    if(n_plate_cnt.any()):
        (x, y, w, h) = cv2.boundingRect(n_plate_cnt)
        license_plate = gray[y:y + h, x:x + w]
        # initialize the reader object
        reader = easyocr.Reader(['ar'])
        # detect the text from the license plate
        detection = reader.readtext(license_plate)
    else :
        detection = []

    if len(detection) == 0:
        # if the text couldn't be read, show a custom message
        text = "Impossible to read the text from the license plate"
        cv2.putText(image, text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 3)
        cv2.imshow('Image', image)
        #cv2.waitKey(0)
    else:
        # draw the contour and write the detected text on the image
        cv2.drawContours(image, [n_plate_cnt], -1, (255, 0, 0), 3)
        

        fontpath = "arial.ttf" # <== download font
        font = ImageFont.truetype(fontpath, 32)
        img_pil = Image.fromarray(image)#create an image object from a numpy array of pixel values.
        draw = ImageDraw.Draw(img_pil)#create a drawing object that will be used to draw on the image.
        text = f"{detection[0][1]} {detection[0][2] * 100:.2f}%"
        reshaped_text = arabic_reshaper.reshape(text)#reshape the text to be rendered in Arabic script.
        bidi_text = get_display(reshaped_text) #applie the bi-directional algorithm to the text to ensure that it is correctly displayed in right-to-left languages like Arabic.
        draw = ImageDraw.Draw(img_pil)
        
        # bidi_text = bidi_text[::-1]
        # print(bidi_text)
        draw.text((x, y - 32),bidi_text, font = font ,fill='red')#draw the text on the image at the specified coordinates ((x, y - 32)) with the specified font (font) and color (fill='red').
        image = np.array(img_pil)#convert the image object back to a numpy array of pixel values.
        

        





        #cv2.putText(image, bidi_text, (x, y - 20),cv2.FONT_HERSHEY_SIMPLEX , 0.75, (0, 255, 0), 2)
        # display the license plate and the output image
        cv2.imshow('license plate', license_plate)
        cv2.imshow('Image', image)
        return detection[0][1]
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
#AI("A3.jpeg")

#vid = cv2.VideoCapture(0)
while(True):
    
    #ret, frame = vid.read()
    #AI(frame)
    #for testing
    try:
        frame = cv2.imread("D2.jpg") #[A3.jpeg,!A2.jpeg,D2.jpg,G2.jpg]
    except:
        break
    text =  AI(frame,False)
    if(not text):
        text = AI(frame,True)
    print(text)
    arabic_nums = "٠١٢٣٤٥٦٧٨٩"
    result_characters = ""
    result_numbers = ""
    if(text):
        for i in range(len(text)):
           
            if text[i] in arabic_nums:
                
                result_characters = text[:i]
                
                result_numbers = text[i:]
                break
    temp = [x for x in result_characters if(x !=" ")]
    result_characters = " ".join(temp)
    result = result_characters + " " + result_numbers
    print(result)
    f = open("Number_plate.txt", 'w', encoding='utf-8')
    
    f.write(result)
    
    f.close()
    cv2.waitKey(10000)
    break
        
    
    
    
    
# frame = cv2.imread("B1.jpeg")
# AI(frame)
# cv2.waitKey(0)
#vid.release()
cv2.destroyAllWindows() 