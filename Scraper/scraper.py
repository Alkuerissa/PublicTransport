import urllib.request
import time
import json
import csv
import datetime
from pathlib import Path

api_key = '123db477-b253-4b8f-a9a1-806bcff0aabe'
data_url = 'https://api.um.warszawa.pl/api/action/wsstore_get/?id=c7238cfe-8b1f-4c38-bb4a-de386db7e776&apikey='
file_name = 'tramwaje.csv'

interval = 30

while 1:
    result = urllib.request.urlopen(data_url + api_key)

    json_result = json.load(result)['result']
    created = not Path(file_name).exists()
    print(datetime.datetime.today().strftime('[%Y-%m-%d %H:%M:%S] Writing... '), end='')

    try:
        with open(file_name, 'a') as result_file:
            csv_file = csv.writer(result_file, lineterminator='\n')
            if created:
                try:
                    csv_file.writerow(json_result[0].keys())
                except IndexError:
                    print('Empty response!', flush=True)
                    continue

            for item in json_result:
                csv_file.writerow(item.values())
        print('OK.', flush=True)
    except IOError:
        print('IO error!', flush=True)
        continue

    time.sleep(interval)
