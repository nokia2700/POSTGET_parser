import csv
import os.path

import requests
from lxml import html

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36'}

res = requests.get('https://www.regard.ru/catalog/1001/protsessory', headers=headers)

dom = html.fromstring(res.content)
lastPage = dom.xpath('//ul[contains(@class,"Pagination_container")]/li[last()]/a/text()')[0]

for page in range(1, int(lastPage) + 1):
    res = requests.get(f'https://www.regard.ru/catalog/1001/protsessory?page={page}', headers=headers)

    dom = html.fromstring(res.content)
    links = dom.xpath('//div[contains(@class,"Card_left")]//h6/../@href')

    for item in links:
        res = requests.get(f'https://www.regard.ru{item}', headers=headers)

        dom = html.fromstring(res.content)

        try:
            model = dom.xpath("//span[contains(text(), 'Модель')]/ancestor::li/p/span/text()")[0]
        except:
            continue

        cores = dom.xpath("//span[contains(text(), 'Количество ядер')]/ancestor::li/p/span/text()")[0]
        frequence = dom.xpath("//span[contains(text(), 'Тактовая частота')]/ancestor::li/p/span/text()")[0]

        file = os.path.join(os.getcwd(), 'data.csv')
        file_exists = os.path.isfile(file)
        fields = ["model", "cores", "frequence"]

        with open(file, 'a', encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fields, delimiter=';')

            if not file_exists:
                writer.writeheader()

            writer.writerow({"model": model, "cores": cores, "frequence": frequence})

    print(f'Распарсили {page} страницу')
