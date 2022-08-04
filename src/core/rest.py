import requests


class RestRequest():
    def __init__(self, url) -> None:
        self._url = url

    def doPost(self,data,headers):
        try:
            request=requests.post(self._url,headers=headers,data=data)
            return request.text
        except Exception as e:
            print(e)
        return None
