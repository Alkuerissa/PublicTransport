import urllib.request
import time
import json
import csv
import datetime
from pathlib import Path

api_key = '123db477-b253-4b8f-a9a1-806bcff0aabe'
data_url_t = 'https://api.um.warszawa.pl/api/action/wsstore_get/?id=c7238cfe-8b1f-4c38-bb4a-de386db7e776&apikey=' + api_key
data_url_a = 'https://api.um.warszawa.pl/api/action/busestrams_get/?resource_id=f2e5503e-927d-4ad3-9500-4ab9e55deb59&type=1&apikey=' + api_key
file_name_t = 'tramwaje.csv'
file_name_a = 'autobusy.csv'

interval = 10
period_t = 3


def load_data(url, file_name, label):
    try:
        print(datetime.datetime.today().strftime('[%Y-%m-%d %H:%M:%S] ') + label, end='')
        result = urllib.request.urlopen(url)
        json_result = json.load(result)['result']
        created = not Path(file_name).exists()

        try:
            with open(file_name, 'a') as result_file:
                csv_file = csv.writer(result_file, lineterminator='\n')
                if created:
                    try:
                        csv_file.writerow(json_result[0].keys())
                    except IndexError:
                        print(' Empty response!', flush=True)
                        return

                for item in json_result:
                    csv_file.writerow(item.values())
            print(' OK.', flush=True)
        except IOError:
            print(' IO error!', flush=True)
            return
    except BaseException:
        print(' Something went wrong!', flush=True)
    return

while 1:
    for i in range(0,period_t):
        load_data(data_url_a, file_name_a, 'Autobusy')
        if i == 0:
            load_data(data_url_t, file_name_t, 'Tramwaje')
        time.sleep(interval)
