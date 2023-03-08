import arabic_reshaper 
from bidi.algorithm import get_display
import numpy as np
from PIL import ImageFont, ImageDraw, Image
import cv2

image =cv2.imread("A1.jpg")
fontpath = "arial.ttf" # <== download font
font = ImageFont.truetype(fontpath, 32)
img_pil = Image.fromarray(image)
draw = ImageDraw.Draw(img_pil)
text="اللغة العربية"
reshaped_text = arabic_reshaper.reshape(text)
bidi_text = get_display(reshaped_text) 
draw = ImageDraw.Draw(img_pil)
print(bidi_text)
bidi_text = bidi_text[::-1]
print(bidi_text)
draw.text((50, 200),bidi_text, font = font ,fill='blue')
image = np.array(img_pil)
cv2.imshow("image with arabic", image) 
cv2.waitKey(0)
cv2.destroyAllWindows()