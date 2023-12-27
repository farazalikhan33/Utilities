import argparse
import requests
from bs4 import BeautifulSoup
import traceback
import json

train_schema = {
    'PADMAVAT-EXPRES-14207',
    'Lucknow-Mail-12229',
    'SATYAGRAH-EXP-15273',
    'LKO-NDLS-AC-SF-12429'
}


class TrainPicker:

    def __init__(self, timeline='1w', start_stn='Shahjehanpur-SPN', destn_stn='New-Delhi-NDLS'):
        self.timeline = timeline
        self.train_list = list()
        self.startstn = start_stn
        self.destn_stn = destn_stn

    def get_trains(self):
        try:
            url = f'https://etrain.info/trains/{self.startstn}-to-{self.destn_stn}'
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                target_block = soup.find('div', class_='trainlist rnd5')

                train_blocks = target_block.find_all('td', class_='wd55')
                for train_block in train_blocks:
                    block = train_block.find('a')
                    if block:
                        train_raw = block.get('href')
                        train = train_raw.replace('/train/', '').replace('/schedule', '')
                        self.train_list.append(train)

                for i, name in enumerate(self.train_list):
                    print(i+1, name)
                return self.train_list

            else:
                return f'Failure fetching trains between {self.startstn} - {self.destn_stn}'
        except Exception as e:
            print(f'Unexpected Error occurred Fetching Train list between - : {e}')
            traceback.print_exc()
            return e


    def get_history(self, train):
        try:
            train_dict = dict()
            url = f'https://etrain.info/train/{train}/history?d={self.timeline}'
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                target_block = soup.find_all('a', class_='runStatStn blocklink rnd5')
                for element in target_block:
                    station_div = element.find('div')
                    if station_div:
                        station_name = station_div.find(text=True, recursive=False).strip()
                        if '(NDLS)' in station_name or '(DLI)' in station_name or '(ANVT)' in station_name:
                            delay = element.find('div', class_='inlineblock pdl5').get_text().split(':')[-1].strip()
                            # train_dict[station_name] = delay
                            return delay
            else:
                return f'received STATUS CODE: {response.status_code} for {train}'
            return train_dict
        except Exception as e:
            print(f'Unexpected Error occurred when fetching info for {train}: {e}')
            traceback.print_exc()
            return e

    def main(self):
        print(f'Picking Train based on last: {self.timeline}\n{self.startstn} to {self.destn_stn}')
        train_list = self.get_trains()
        train_info = dict()
        for train in train_list:
            delay_chart = self.get_history(train)
            train_info[train] = delay_chart

        pretty_info = json.dumps(train_info, indent=4)
        print(f'Showing train based on average delay for the last {self.timeline}\n{pretty_info}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train Picker CLI')
    parser.add_argument('--timeline', type=str, choices=['1w', '1m', '3m', '6m'],
                        help='Timeline: 1w for 1 week, 1m for 1 month, 3m for 3 months, and 6m for 6 months')
    parser.add_argument('--start-stn', type=str, required=True,
                        help='Starting station in the format First-Word-Second-Word...-Station-Code | ex: '
                             'Chandigarh-CDG')
    parser.add_argument('--destn-stn', type=str, required=True,
                        help='Destination station in the format First-Word-Second-Word...-Station-Code | ex: '
                             'NEW-DELHI-NDLS')

    args = parser.parse_args()
    obj = TrainPicker(timeline=args.timeline, start_stn=args.start_stn, destn_stn=args.destn_stn)
    obj.main()

