import argparse
import imutils
import cv2

#Argument Parser
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str,
	help="path to input video file")
args = vars(ap.parse_args())

#Using CSRT Open CV object tracker

trackers = cv2.legacy.MultiTracker_create()

#Video stream
vs = cv2.VideoCapture(args["video"])

#Constantly refresh frames
while True:
    #Read the next frame
	grabbed, frame = vs.read()

	#Check for the end
	if frame is None:
		break

	#Resize the frame
	frame = imutils.resize(frame, width=600)

	#Grab updated bounding boxes coordinates
	(success, boxes) = trackers.update(frame)

	#Loop over the bounding boxes and draw then on the frame
	for box in boxes:
		(x, y, w, h) = [int(v) for v in box]
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

	#Show the output frame
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(33) & 0xFF

	#If the 's' key is selected, choose a bounding box to track
	if key == ord("s"):
		box = cv2.selectROI("Frame", frame, fromCenter=False,
			showCrosshair=True)

		#Directly create a CSRT tracker
		tracker = cv2.legacy.TrackerCSRT_create()
		trackers.add(tracker, frame, box)

	#End
	elif key == ord("q"):
	    break


#Close windows
vs.release()
cv2.destroyAllWindows()

"""
HOW TO RUN THIS PROGRAM:

1. Find your own clip to use
2. Run this program in your terminal
3. Click 's' and drag with your crosshair to track
4. Click the SPACE BAR to continue
5. Repeat steps 3-4 track multiple objects

Example:
bash: python3 object_tracking.py --video clip.mp4
"""