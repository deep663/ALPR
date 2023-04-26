import cv2
import numpy as np
import imutils
import pytesseract
import tkinter as tk

win = tk.Tk()
win.title("Licence plate Detection")


path = [r'C:\Users\deeps\Desktop\vs_code\python\vehicaleLicensePlateDetection\test_items\dataset-card.jpg',
        r'C:\Users\deeps\Desktop\vs_code\python\vehicaleLicensePlateDetection\test_items\numberplate.jpg']

img = cv2.imread(path[0])
img = imutils.resize(img, width=600)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# cv2.imshow("Grayscale", gray)
# cv2.waitKey(0)


bfilter = cv2.bilateralFilter(gray, 11, 17, 17)
edge = cv2.Canny(bfilter, 30, 200)
# cv2.imshow("Canny",edge)

# Finding Edges on the image
keypoints = cv2.findContours(
    edge.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(keypoints)
contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

cv2.drawContours(img.copy(),contours,-1,(0,255,0),3)
# cv2.imshow("contours",img)
# cv2.waitKey(0)

# filtering posible shapes for Licence plate
location = None
for c in contours:
    approx = cv2.approxPolyDP(c, 20, True)
    if len(approx) == 4:
        location = approx
        break

# masking out the Licence plate
mask = np.zeros(gray.shape, np.uint8)
new_img = cv2.drawContours(mask, [location], 0, 255, -1)
new_img = cv2.bitwise_and(img, img, mask=mask)
# cv2.imshow("Licence Plate", new_img)

# croping the licence plate 
(x, y) = np.where(mask == 255)
(x1, y1) = (np.min(x), np.min(y))
(x2, y2) = (np.max(x), np.max(y))
crop_img = gray[x1:x2+1, y1:y2+1]
rectKern = cv2.getStructuringElement(cv2.MORPH_RECT, (13, 5))
blackhat = cv2.morphologyEx(crop_img, cv2.MORPH_BLACKHAT, rectKern)
cv2.imshow("Croped Licence Plate", crop_img)


# Bulding options for OCR
def build_tesseract_options(psm=7):
    alphanumeric = "ABCDEFGHIKLMNOPQRSTUVWXYZ0123456789"
    options = "-c tessedit_char_whitelist={}".format(alphanumeric)
    options += " --psm {}".format(psm)
    return options


# strip out non-ASCII text so we can draw the text on the image using OpenCV
def cleanup_text(text):
    return "".join([c if ord(c) < 128 else "" for c in text]).strip()


# OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
options = build_tesseract_options()
lpText = pytesseract.image_to_string(blackhat, config=options)

# draw the bounding box on the license plate
res = cv2.rectangle(img, tuple(approx[0][0]), tuple(
    approx[2][0]), (0, 255, 0), 3)
# compute a normal (unrotated) bounding box for the license plate and then draw the OCR'd license plate text on the image
res = cv2.putText(img, cleanup_text(lpText), org=(
    approx[0][0][0], approx[1][0][1]+60), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0, 255, 0), thickness=3)

# print the licence plate Number
print("[LICENCE PLATE INFO] {}".format(lpText))

# noPlates = []
# noPlates.append(lpText)

# file = open(r'C:\Users\deeps\Desktop\vs_code\python\vehicaleLicensePlateDetection\LicencePlaeNos.txt', 'a') 
# for line in noPlates:  
#     file.write(line) 

#Display the detected Licence plate number
cv2.imshow("Licence Plate No:", res)
cv2.waitKey(0)

butn = tk.Button(win,text='Exit', width=15, command=win.destroy)
butn.pack()
win.mainloop()
