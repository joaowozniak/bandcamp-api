import requests


class Utils:
    @staticmethod
    def execute_post_request(url, body):
        response = requests.post(
            url,
            data=body,
            headers={"Content-Type": "application/json"},
        )
        return response

    @staticmethod
    def execute_get_request(url):
        response = requests.get(
            url,
            headers={"Content-Type": "application/json"},
        )
        return response
