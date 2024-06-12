from io import RawIOBase
from requests.api import head
import time, lxml, json, csv, requests, os
from progress.bar import ChargingBar

headers = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Content-Type": "text/html",
}

urls = []
# https://api.staff-clothes.com/api/v2/product/by-consumer-category/1207eb2e-b501-4dec-9dcf-e870f06f0ce5?access_token=MDFiNjdiNGFhZjU4ZDU0YzVkMjQ4NDMxYTI5YWM0Y2QzZjQzNjJhYjI4ZjY1ODJlOTZjN2QxMmQxNjM2OTMyNQ&locale=ua&shortSlug=m&categoryName=shorty&categoryCode=c1029&limit=24&offset=0&category=c1694512-f78b-11e5-bac8-d43d7eea3243
access_token = 'MDFiNjdiNGFhZjU4ZDU0YzVkMjQ4NDMxYTI5YWM0Y2QzZjQzNjJhYjI4ZjY1ODJlOTZjN2QxMmQxNjM2OTMyNQ'
url = 'https://api.staff-clothes.com/api/v2/product/by-consumer-category/1207eb2e-b501-4dec-9dcf-e870f06f0ce5?access_token={}&locale=ua&shortSlug=m&categoryName=shorty&categoryCode=c1029&limit=24&offset={}&category=c1694512-f78b-11e5-bac8-d43d7eea3243'
with open('shorts.csv', 'w') as file:
    writer = csv.writer(file, dialect='excel', delimiter = '|')
    headers_ = [
        'Title',
        'Price',
        'Article',
        'Sizes',
        'URL',
        ]

    writer.writerows([headers_])

process = ''

bar = ChargingBar('Parsing data  ', max=100, suffix='%(percent)d%%')

offset = 0
c = 1

while True:

    req = requests.get(url = url.format(access_token, offset), headers=headers)

    with open('data_{}.json'.format(offset), 'w') as file:
        file.write(req.text)

    with open('data_{}.json'.format(offset), 'r') as file:
        
        cloth_list = json.load(file)
        
        if cloth_list:

            with open('shorts.csv', 'a') as file_csv:
                writer = csv.writer(file_csv, dialect='excel', delimiter = '|')

                with open('shorts.json', 'w') as file_json:

                    for cloth in cloth_list:

                        sizes = ''
                        for dt in cloth['sizes']:
                            sizes += ':'.join([str(value) for value in dt.values()]) + ', '

                        data = [
                            bytes(cloth['title'], encoding='unicode-escape').decode('unicode-escape'),
                            cloth['price'],
                            cloth['article'],
                            sizes[0:-3],
                            'https://www.staff-clothes.com' + cloth['productSiteUrlShortV2'].strip('\\'),
                            ]

                        data_json = {
                            # 'Title': bytes(cloth['title'], encoding='unicode-escape').decode('unicode-escape'),
                            'Title': 'То є україньский тайтл',
                            'Price': cloth['price'],
                            'Article': cloth['article'],
                            'Sizes': sizes[0:-3],
                            'URL': 'https://www.staff-clothes.com' + cloth['productSiteUrlShortV2'].strip('\\'),
                        }

                        d = json.dumps(data_json, indent=4)
                        file_json.write(d)

                        writer.writerows([data])
        else:
            break
    
    c+=1
    bar.next(100/c)
    offset += 24
    
bar.next(100)

for number in range(0, offset + 1, 24): os.remove(f'data_{number}.json')


        
