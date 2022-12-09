import requests
import lxml
from bs4 import BeautifulSoup
import json
import collections
import pprint as pp
import operator
import re

# define request

req = {
    "q": "talabarteria monterrey empresas"
}


def get_business_data(request):
    params = {
            "q": req["q"],
            "tbm": "lcl"
        }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome"
                      "/105.0.0.0 Safari/537.36"
    }

    html = requests.get("https://www.google.com/search", params=params, headers=headers)
    soup = BeautifulSoup(html.text, "lxml")
    rsp = {"status": 200, "data": []}
    for idx, result in enumerate(soup.select(".a-no-hover-decoration")):
        info = []
        for res in result.select("div"):
            info.append(res.text)
        try:
            name = info[2]
            rating = info[3].split("·")[0].strip()
            business_type = info[3].split("·")[-1].strip()
        except IndexError:
            rsp = {"status": 400, "data": []}
            break

        if business_type == "No hay opiniones.":
            business_type = "Unknown"

        address_telephone = info[4].split("·")

        if len(address_telephone) == 2:
            address = address_telephone[0].strip()
            telephone = address_telephone[1].strip()
        else:
            address = address_telephone[0].strip()
            telephone = "Unknown"

        data = {
            "name": name,
            "rating": rating,
            "business_type": business_type,
            "address": address,
            "telephone": telephone
        }

        rsp["data"].append(data)
    return rsp


response = get_business_data(req)
pp.pprint(response)


