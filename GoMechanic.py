import os
import json
import requests


BRAND_URL = "https://gomechanic.in/api/v1/get-brands"
ADD_CARS_API = "http://192.168.29.211:8000/car/add-cars"
ADD_BRAND_API = "http://192.168.29.211:8000/car/add-brands"
MODEL_URL = "https://gomechanic.app/api/v2/oauth/vehicles/get_models_by_brand"

class RequestHandler:
	def get_brands(self):
		self.brandsReq = requests.get(BRAND_URL)
		self.brands = json.loads(self.brandsReq.content.decode("utf-8"))["data"]
		return self.brands

	def fetch_models(self, id):
		self.modelsReq = requests.get(f"{MODEL_URL}/?brand_id={id}")
		self.models = json.loads(self.modelsReq.content.decode("utf-8"))["data"]
		return self.models


def main():
	rh = RequestHandler()
	brands = rh.get_brands()
	print("[+] Fetched all brands\n")
	for obj in brands:
		brandsReq = requests.post(ADD_BRAND_API, json={
			"name": obj['name'],
			"logo": obj['icon']
		})
		if brandsReq.status_code != 200:
			print()
			print(brandsReq.content)
			print()
			print("[-] Something went wrong")
			break

		brandID = json.loads(brandsReq.content.decode("utf-8"))["data"]["id"]
		print(f"\n[+] {obj['name']} brand added to cswDB")
		models = rh.fetch_models(obj["id"])
		print(f"\t[+] Fetched all models of {obj['name']}")
		modelData = []
		for model in models:
			modelData.append({
				"model": model["name"],
				"image": model["image_path"],
				"type": "Petrol"
			})
			modelData.append({
				"model": model["name"],
				"image": model["image_path"],
				"type": "Diesel"
			})
			modelData.append({
				"model": model["name"],
				"image": model["image_path"],
				"type": "CNG"
			})

		carReq = requests.post(ADD_CARS_API, json={
			"brandID": brandID,
			"Cars": modelData
		})
		if carReq.status_code != 200:
			print()
			print(carReq.content)
			print()
			print("[-] Something went wrong")
			break

		print(f"\t[+] All models of {obj['name']} added to cswDB\m")


if __name__ == "__main__": 
	main()