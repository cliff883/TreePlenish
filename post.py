import requests

url = "http://143.215.91.126:8000/predict"

with open("image.jpg", 'rb') as image_file:
	response = requests.post(url, files={'image': image_file})

result = response.json()
print(result.keys())
