import requests
import lxml
from bs4 import BeautifulSoup
import json
import collections
import pprint as pp
import operator


def get_data(req):
    params = {
        "q": req["q"],
        "tbm": "shop"
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome"
                      "/105.0.0.0 Safari/537.36"
    }

    html = requests.get("https://www.google.com/search", params=params, headers=headers)
    soup = BeautifulSoup(html.text, "lxml")

    data = []
    for result in soup.select(".i0X6df"):
        title = result.select_one(".translate-content").text
        price = result.select_one(".OFFNJ").text
        seller = result.select_one(".IuHnof").text
        delivery = result.select_one(".vEjMR").text
        link = f"https://www.google.com{result.select_one('.Lq5OHe.eaGTj')['href']}"

        data.append({
            "title": title,
            "price": price,
            "seller": seller,
            "delivery": delivery,
            "link": link
        })
    return data


# Bar
def get_price_data(d):
    prices = {
        '0-100': {},
        '100-200': {},
        '200-300': {},
        '300-400': {},
        '400-500': {},
        '500-600': {},
        '600-700': {},
        '700-800': {},
        '800-900': {},
        '900-1000': {},
        '1000-2000': {},
        '2000-3000': {},
        '3000-4000': {},
        '4000-5000': {},
        '5000-6000': {},
        '6000-7000': {},
        '7000-8000': {},
        '8000-9000': {},
        '9000-10000': {},
        '10000+': {}
    }

    bounds = [
        0, 100, 200, 300, 400, 500, 600, 700, 800, 900,
        1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000,
        10000
    ]

    for obj in data:
        if 'mensuales' in obj['price']:
            continue

        currency, price = obj['price'].split()
        price = float(price.replace(',', ''))

        for idx, lower_bound in enumerate(bounds[0:-1]):
            higher_bound = bounds[idx+1]
            if lower_bound < price < higher_bound:
                if obj['seller'] in prices[f'{lower_bound}-{higher_bound}'].keys():
                    prices[f'{lower_bound}-{higher_bound}'][obj['seller']] += 1
                else:
                    prices[f'{lower_bound}-{higher_bound}'][obj['seller']] = 1

        if price > 10000:
            if obj['seller'] in prices['10000+'].keys():
                prices['10000+'][obj['seller']] += 1
            else:
                prices['10000+'][obj['seller']] = 1

    p = {}
    for price_range in prices:
        if not prices[price_range]:
            continue
        p[price_range] = prices[price_range]

    for price_range in p:
        p[price_range] = dict(sorted(p[price_range].items(), key=operator.itemgetter(1), reverse=True))

    colors = [
        'hsl(123, 100%, 60%)',
        'hsl(63, 100%, 58%)',
        'hsl(41, 100%, 50%)',
        'hsl(12, 100%, 50%)',
        'hsl(318, 100%, 67%)',
        'hsl(254, 100%, 67%)',
        'hsl(195, 100%, 52%)',
        'hsl(174, 100%, 50%)',
    ]
    bars = []
    keys = []
    for price_range in p:
        bar = {'precio': price_range}
        otros = 0
        color_idx = 0
        for idx, seller in enumerate(p[price_range]):
            if idx <= 5:
                bar[seller] = p[price_range][seller]
                bar[seller + 'Color'] = colors[color_idx]
                keys.append(seller)
                color_idx += 1
            else:
                otros += p[price_range][seller]

        bar['otros'] = otros
        bar['otrosColor'] = colors[5]
        bars.append(bar)

    keys.append('otros')
    keys = list(dict.fromkeys(keys))

    for bar in bars:
        for seller in keys:
            if seller not in bar:
                bar[seller] = 0
                bar[seller + 'Color'] = 'hsl(0, 0%, 0%)'

    return keys, bars


# Funnel
def get_word_data(d, word_amount):
    w = ""
    for obj in d:
        w += obj['title']

    word_count = dict(collections.Counter(w.split()))

    w = []
    count = []

    for key in word_count:
        w.append(key)
        count.append(word_count[key])

    max_value = max(count)
    max_index = count.index(max_value)

    top_w = {}
    for i in range(word_amount):
        max_value = max(count)
        max_index = count.index(max_value)
        top_w[w[max_index]] = count[max_index]
        count.pop(max_index)
        w.pop(max_index)

    top_w_data = []
    for word in top_w:
        w_data = {
            'id': f'step_{word}',
            'value': top_w[word],
            'label': word
        }
        top_w_data.append(w_data)

    return top_w_data


# Pie
def top_sellers_data(d, seller_amount):
    s = []
    for obj in d:
        s.append(obj['seller'])

    seller_count = dict(collections.Counter(s))
    s = []
    count = []

    for key in seller_count:
        s.append(key)
        count.append(seller_count[key])

    colors = [
        'hsl(123, 100%, 60%)',
        'hsl(63, 100%, 58%)',
        'hsl(41, 100%, 50%)',
        'hsl(12, 100%, 50%)',
        'hsl(318, 100%, 67%)',
        'hsl(254, 100%, 67%)',
        'hsl(195, 100%, 52%)',
        'hsl(174, 100%, 50%)',
    ]
    top_s = []
    for i in range(seller_amount):
        max_value = max(count)
        max_index = count.index(max_value)

        ID = s[max_index]
        label = s[max_index]
        value = count[max_index]

        seller_info = {
            "id": ID,
            "label": label,
            "value": value,
            "color": colors[i]
        }

        top_s.append(seller_info)
        count.pop(max_index)
        s.pop(max_index)

    return top_s


# Bar
def get_delivery_data(d):
    dels = {
        "Envío gratuito": {},
        "+ envío": {},
    }

    for obj in data:
        if obj['delivery'] == "Envío gratuito":
            if obj['seller'] in dels["Envío gratuito"].keys():
                dels['Envío gratuito'][obj['seller']] += 1
            else:
                dels['Envío gratuito'][obj['seller']] = 1

        elif obj['delivery'].startswith('+'):
            if obj['seller'] in dels["+ envío"].keys():
                dels['+ envío'][obj['seller']] += 1
            else:
                dels['+ envío'][obj['seller']] = 1

    for delivery_type in dels:
        dels[delivery_type] = dict(sorted(dels[delivery_type].items(), key=operator.itemgetter(1), reverse=True))

    colors = [
        'hsl(123, 100%, 60%)',
        'hsl(63, 100%, 58%)',
        'hsl(41, 100%, 50%)',
        'hsl(12, 100%, 50%)',
        'hsl(318, 100%, 67%)',
        'hsl(254, 100%, 67%)',
        'hsl(195, 100%, 52%)',
        'hsl(174, 100%, 50%)',
    ]
    bars = []
    keys = []
    for delivery_type in dels:
        bar = {'tipo de envío': delivery_type}
        otros = 0
        color_idx = 0
        for idx, seller in enumerate(dels[delivery_type]):
            if idx <= 5:
                bar[seller] = dels[delivery_type][seller]
                bar[seller + 'Color'] = colors[color_idx]
                keys.append(seller)
                color_idx += 1
            else:
                otros += dels[delivery_type][seller]

        bar['otros'] = otros
        bar['otrosColor'] = colors[5]
        bars.append(bar)

    keys.append('otros')
    keys = list(dict.fromkeys(keys))

    for bar in bars:
        for seller in keys:
            if seller not in bar:
                bar[seller] = 0
                bar[seller + 'Color'] = 'hsl(0, 0%, 0%)'

    return keys, bars


# Define request
request = {
    "q": "playera tigres"
}

# Get initial data
data = get_data(request)

# Get price data
price_keys, price_data = get_price_data(data)

# get deliveries
delivery_keys, delivery_data = get_delivery_data(data)

# Get top sellers
sellers_data = top_sellers_data(data, 5)

# Get top words
word_data = get_word_data(data, 6)


response = {
    'price_bar_graph': {
        'data': price_data,
        'keys': price_keys,
    },
    'delivery_bar_graph': {
        'data': delivery_data,
        'keys': delivery_keys,
    },
    'seller_pie_chart': {
        'data': sellers_data
    },
    'word_funnel_chart': {
        'data': word_data
    }
}

pp.pprint(response)

