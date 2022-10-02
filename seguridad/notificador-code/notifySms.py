import requests

class SmsNotificator():

    def send_sms(telephone, message):

        SMPP_URL = 'https://sms.frankpaul.co/Api/rest/message'

        headers = {"Content-Type": "application/json", "Authorization" : "Basic bWlzby1lcXVpcG8zMDpENjYyS2NLMw=="}

        data = {"to":[f"{telephone}"],"text":f'{message}',"from":"Alert"}
        r = requests.get(SMPP_URL, headers=headers , json=data)
        print(r)