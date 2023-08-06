from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
import numpy as np
import argparse
import time
import cv2
import os
import matplotlib.pyplot as plt
import sys
#from pretrained_models import get_model

def detect_and_predict_mask(frame, faceNet, maskNet, args):
	# grab the dimensions of the frame and then construct a blob
	# from it
	(h, w) = frame.shape[:2]
	blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300),
		(104.0, 177.0, 123.0))

	# pass the blob through the network and obtain the face detections
	faceNet.setInput(blob)
	detections = faceNet.forward()

	# initialize our list of faces, their corresponding locations,
	# and the list of predictions from our face mask network
	faces = []
	locs = []
	preds = []

	# loop over the detections
	for i in range(0, detections.shape[2]):
		# extract the confidence (i.e., probability) associated with
		# the detection
		confidence = detections[0, 0, i, 2]

		# filter out weak detections by ensuring the confidence is
		# greater than the minimum confidence
		if confidence > args["confidence"]:
			# compute the (x, y)-coordinates of the bounding box for
			# the object
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")

			# ensure the bounding boxes fall within the dimensions of
			# the frame
			(startX, startY) = (max(0, startX), max(0, startY))
			(endX, endY) = (min(w - 1, endX), min(h - 1, endY))

			# extract the face ROI, convert it from BGR to RGB channel
			# ordering, resize it to 224x224, and preprocess it
			face = frame[startY:endY, startX:endX]
			face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
			face = cv2.resize(face, (224, 224))
			face = img_to_array(face)
			face = preprocess_input(face)

			# add the face and bounding boxes to their respective
			# lists
			faces.append(face)
			locs.append((startX, startY, endX, endY))

	# only make a predictions if at least one face was detected
	if len(faces) > 0:
		# for faster inference we'll make batch predictions on *all*
		# faces at the same time rather than one-by-one predictions
		# in the above `for` loop
		faces = np.array(faces, dtype="float32")
		preds = maskNet.predict(faces, batch_size=32)

	# return a 2-tuple of the face locations and their corresponding
	# locations
	return (locs, preds)

def get_args():
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True,
	    help="path to input image")
    ap.add_argument("-f", "--face", type=str,
	    default="models",
	    help="path to face detector model directory")
    ap.add_argument("-m", "--model", type=str,
	    default="models/helmet_detector.h5",
	    help="path to trained helmet detector model")
    ap.add_argument("-o", "--output", 
        default="file", type=str,
        help="image output to file or screen")
    ap.add_argument("-c", "--confidence", type=float, default=0.5,
	    help="minimum probability to filter weak detections")
    args = vars(ap.parse_args())
    return args

def main():
    #get_model()
    print('Downloading models ...')
    args = get_args()
    # load our serialized face detector model from disk
    print("Loading face detector model...")
    prototxtPath = os.path.sep.join([args["face"], "deploy.prototxt"])
    #print(f'Path : {prototxtPath}')
    weightsPath = os.path.sep.join([args["face"],
        "res10_300x300_ssd_iter_140000.caffemodel"])
    #print(f'Weights path : {weightsPath}')
    faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)

    # load the face mask detector model from disk
    print("Loading helmet detector model...")
    maskNet = load_model(args["model"])

    # load the input image from disk, clone it, and grab the image spatial
    # dimensions
    image = cv2.imread(args["image"])
    mask_found = False

    exit_txt = '''
    ********************************************************
    *** No valid image detected. Try again. Quitting ... ***
    ********************************************************
    ''' 

    if image is None:
        print(exit_txt)
        sys.exit(0)

    orig = image.copy()
    (h, w) = image.shape[:2]

    # construct a blob from the image
    blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300),
        (104.0, 177.0, 123.0))

    # pass the blob through the network and obtain the face detections
    faceNet.setInput(blob)
    detections = faceNet.forward()

    # loop over the detections
    for i in range(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with
        # the detection
        confidence = detections[0, 0, i, 2]

        # filter out weak detections by ensuring the confidence is
        # greater than the minimum confidence
        if confidence > args["confidence"]:
            # compute the (x, y)-coordinates of the bounding box for
            # the object
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # ensure the bounding boxes fall within the dimensions of
            # the frame
            (startX, startY) = (max(0, startX), max(0, startY))
            (endX, endY) = (min(w - 1, endX), min(h - 1, endY))

            # extract the face ROI, convert it from BGR to RGB channel
            # ordering, resize it to 224x224, and preprocess it
            face = image[startY:endY, startX:endX]
            face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            face = cv2.resize(face, (224, 224))
            face = img_to_array(face)
            face = preprocess_input(face)
            face = np.expand_dims(face, axis=0)

            # pass the face through the model to determine if the face
            # has a mask or not
            (mask, withoutMask) = maskNet.predict(face)[0]

            # determine the class label and color we'll use to draw
            # the bounding box and text
            label = "Helmet" if mask > withoutMask else "No Helmet"
            color = (0, 0, 255) if label == "Helmet" else (0, 255, 0)

            # include the probability in the label
            label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)

            # display the label and bounding box rectangle on the output
            # frame
            if mask > withoutMask:
                mask_found = True
                cv2.putText(image, label, (startX, startY - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 2)
                cv2.rectangle(image, (startX, startY), (endX, endY), color, 2)
            else:
                cv2.putText(image, "No helmet detected", (startX, startY - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 1)
    # show the output image depending on output
    output_file = 'image.jpg'
    original_file = 'original_image.jpg'
    mask_txt = '''
    *****************************************************************************
    ******************************* HELMET DETECTED *****************************
    *****************************************************************************
    '''
    no_mask_txt = '''
    *****************************************************************************
    ***************************** NO HELMET DETECTED ****************************
    *****************************************************************************
    '''
    if args["output"] == 'file':
        print(f'Writing out to {output_file}')
        cv2.imwrite(output_file, image)
        cv2.imwrite(original_file, orig)
        if mask_found:
            print(mask_txt)
        else:
            print(no_mask_txt)
    else:
        print(f'Writing out to display')
        if mask_found:
            print(mask_txt)
        else:
            print(no_mask_txt)
        cv2.imshow("Output", image)
        cv2.waitKey(0)
    
if __name__ == '__main__':
    main()