import requests
import os
import sys

location = os.getcwd()
print(location)
sys.path.append(location)

from Utilities.telegram import send_message

def get_pnr(pnr):
    message = str()
    response = requests.get(f'https://www.redbus.in/railways/api/getPnrData?pnrno={pnr}')
    if response.status_code == 200:
        response_json = response.json()
        passenger_detail = response_json['passengers'][-1]
        status = passenger_detail['currentStatus']
        seat_detail = passenger_detail['currentSeatDetails']
        current_status = f'{status} - {seat_detail}'
        if status == 'Waitlist':
            confirmation_prob = passenger_detail['confirmProb']
            char_prep_time = f"{response_json['chartStatus']}"
            if char_prep_time == 'Chart Not Prepared':
                char_prep_time += f'\n{response_json["chartPrepMsg"]}'
            current_status += f'\nConfirmation chances: {confirmation_prob}%\nChart Prep: {char_prep_time}'

        message += f'*PNR: {pnr} | {response_json["srcCode"]}(PF: {response_json["srcPfNo"]}) to ' \
                   f'{response_json["dstCode"]}(PF: {response_json["dstPfNo"]})\n*'
        message += f'{response_json["overallStatus"]} for ({response_json["trainNumber"]})\n'
        message += f'Current Status: {current_status}\n'
        print(message)
        return message


result = get_pnr('2755291763')
if result:
    send_message(result, alert_test_channel=True)
