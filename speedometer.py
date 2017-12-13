from PIL import Image
import pytesseract
from PIL import ImageGrab


screen_image = ImageGrab.grab(bbox=(0,40,800,640))

print(pytesseract.image_to_string(Image.open('Capture.PNG')))