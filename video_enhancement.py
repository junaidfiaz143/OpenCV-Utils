import numpy as np
import cv2
from PIL import ImageEnhance
import argparse

ap = argparse.ArgumentParser(description="")

ap.add_argument("-i", "--input", type=str, default="0", help="path to input video file")

args = vars(ap.parse_args())

if args["input"] != "0":
    cap = cv2.VideoCapture(args["input"])
else:
    cap = cv2.VideoCapture(0)

image_counter = counter = 0

while(cap.isOpened()):

    ret, frame = cap.read()

    try:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    except:
        break
    cv2.namedWindow('Gray', cv2.WINDOW_NORMAL)
    cv2.imshow('Gray', gray)

    equ = cv2.equalizeHist(gray)
    cv2.namedWindow('Equalized', cv2.WINDOW_NORMAL)
    cv2.imshow('Equalized', equ)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cl1 = clahe.apply(gray)
    cv2.namedWindow('Clahe', cv2.WINDOW_NORMAL)
    cv2.imshow('Clahe', cl1)

    cv2.namedWindow('Original', cv2.WINDOW_NORMAL)
    cv2.imshow('Original', frame)

    counter += 1

    if counter%5 == 0:

        image_counter += 1

        gray_name = args["input"][: -4]+"/Gray/"+args["input"].split(".")[0]+"-gray" + '-' + str(image_counter) + ".png"
        cv2.imwrite(gray_name, gray)

        equalized_name = args["input"][: -4]+"/Equalized/"+args["input"].split(".")[0]+"-equalized" + '-' + str(image_counter) + ".png"
        cv2.imwrite(equalized_name, equ)

        clahe_name = args["input"][: -4]+"/Clahe/"+args["input"].split(".")[0]+"-clahe" + '-' + str(image_counter) + ".png"
        cv2.imwrite(clahe_name, cl1)

        original_name = args["input"][: -4]+"/Original/"+args["input"].split(".")[0]+"-original" + '-' + str(image_counter) + ".png"
        cv2.imwrite(original_name, frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

if args["input"] != "0":
    print("["+args["input"]+"] Successfully converted into frames.")
else:
    print("[RECORDING] Successfully converted into frames.")

cap.release()
cv2.destroyAllWindows()