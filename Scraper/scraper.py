import urllib.request
import time
import json
import csv
import os

api_key = '123db477-b253-4b8f-a9a1-806bcff0aabe'
data_url = 'https://api.um.warszawa.pl/api/action/wsstore_get/?id=c7238cfe-8b1f-4c38-bb4a-de386db7e776&apikey='
file_name = 'tramwaje.csv'

interval = 30

while 1:
    result = urllib.request.urlopen(data_url + api_key)

    json_result = json.load(result)['result']
    created = ~(os.path.isfile(file_name))

    with open(file_name, 'w') as result_file:
        csv_file = csv.writer(result_file, lineterminator='\n')
        if created:
            csv_file.writerow(json_result[0].keys())
        for item in json_result:
            csv_file.writerow(item.values())

    time.sleep(interval)
