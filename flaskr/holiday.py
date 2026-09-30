import requests

def get_holidays():
    """
    日本の祝日を取得する。
    """
    
    url = "https://holidays-jp.github.io/api/v1/date.json"
    response = requests.get(url)
    holidays = response.json()
    return holidays