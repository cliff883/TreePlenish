from cv2 import *
import time
import serial
import requests

#send request to ML model url
url = "http://143.215.91.126:5000/predict"

cam_port = -1



while True:
	print("capturing image")
	start = time.time()
	cam = VideoCapture(cam_port)
	result, image = cam.read()

	if result:
		#image = cvtColor(image, COLOR_BGR2GRAY)
		imwrite("/home/raspberry/recycle/image.jpg", image)
	else:
		print("nothing detected")
		exit(0)



	with open("image.jpg", 'rb') as image_file:
		response = requests.post(url, files={'image': image_file})

	result = response.json()
	end = time.time()
	print(result)
	print(end - start, " seconds to execute")

	imshow("abcd", image)
	waitKey(0)
	destroyWindow("abcd")
	
	s = input("b to end")
	if s == "b":
		break
	else:
		del cam
		continue
