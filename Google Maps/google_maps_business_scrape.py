import requests
from bs4 import BeautifulSoup
import pprint as pp
import json
from fake_useragent import UserAgent


def get_business_data(request):
    rsp = {"status": 200, "data": []}
    k_word = request["keyword"]
    cty = request["city"]

    q = f"{k_word} {cty}"
    ua = UserAgent()
    user_agent = ua.random
    user_agent = ua.random

    for i in range(10):
        params = {
            "q": q,
            "tbm": "lcl",
            "start": f"{i * 20}"
        }

        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
            'referer': 'https://www.google.com/'
        }

        html = requests.get("https://www.google.com/search", params=params, headers=headers)
        soup = BeautifulSoup(html.text, "html.parser")
        pp.pprint(soup)
        for idx, result in enumerate(soup.select(".a-no-hover-decoration")):
            info = []
            for res in result.select("div"):
                info.append(res.text)

            try:
                name = info[2]
                rating = info[3].split("·")[0].strip()
                business_type = info[3].split("·")[-1].strip()
            except IndexError:
                continue

            if business_type == "No hay opiniones.":
                business_type = "Unknown"
            try:
                address_telephone = info[4].split("·")
                if len(address_telephone) >= 2:
                    address = address_telephone[0].strip()
                    telephone = address_telephone[1].strip()
                else:
                    address = address_telephone[0].strip()
                    telephone = "Unknown"
            except IndexError:
                address = "Unknown"
                telephone = "Unknown"

            data = {
                "keyword": k_word,
                "name": name,
                "rating": rating,
                "business_type": business_type,
                "address": address,
                "telephone": telephone

            }

            rsp["data"].append(data)

    return rsp


# Define keywords
keywords = ['joyas',
            'playeras',
            'gorras',
            'sexshop',
            'vape',
            'lentes',
            'anillos',
            'regalos',
            'novedades',
            'papeleria',
            'ropa',
            'vestidos',
            'fajas',
            'suplementos',
            'juguetes',
            'libros',
            'dulces',
            'talabarteria',
            'imprenta',
            'tenis',
            'zapatos',
            'esoteria',
            'velas',
            'cuarzos',
            'mochilas']
cities = ["mty", "cdmx"]

# Current keyword
keyword = keywords[7]
city = cities[0]
print(keyword)

req = {
    "keyword": keyword,
    "city": city,
}
response = get_business_data(req)
num_scrape = len(response["data"])
print(f"---- {keyword} scraped ---- {num_scrape} results found ----")

with open("gmbs_data.json", 'r+') as file:
    existing_data = json.load(file)
    for entry in response["data"]:
        if entry not in existing_data:
            existing_data.append(entry)
    file.seek(0)
    json.dump(existing_data, file, indent=4)

