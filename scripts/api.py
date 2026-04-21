import requests

api_key = "e800f58ce07f5664f2c7d703e5427627"

url = f"https://api.themoviedb.org/3/movie/550?api_key={api_key}"
response = requests.get(url)

data = response.json()
print(data.keys())