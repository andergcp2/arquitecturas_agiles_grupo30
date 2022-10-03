import requests

class SmsNotificator():

    def send_sms(self, telephone, message):

        SMPP_URL = 'https://sms.frankpaul.co/Api/rest/message'

        headers = {"Content-Type": "application/json", "Authorization" : "Basic bWlzby1lcXVpcG8zMDpENjYyS2NLMw=="}

        data = {"to":[f"{telephone}"],"text":f'{message}',"from":"130232"}
        print(f"Enviando mensaje: {message} : to {telephone}")
        r = requests.get(SMPP_URL, headers=headers , json=data)
        print(r)