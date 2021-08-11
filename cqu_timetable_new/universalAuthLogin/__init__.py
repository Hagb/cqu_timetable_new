from cqu_timetable_new.universalAuthLogin.universalAuthLogin import getLoginData
from cqu_timetable_new.universalAuthLogin.utils import getAccessTokenDict
import requests
import json


def get_timetable_by_request():
    """Get timetable using requests
    :exception Network Error
                Server Error
    :return: json
    """
    enroll_api = 'http://my.cqu.edu.cn/enroll-api/timetable/student/' + ""
    ua = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
    headers = {
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
    }
    session = getLoginData(,)

    auth = getAccessTokenDict(session)['Authorization']
    headers["User-Agent"] = ua
    headers["Authorization"] = auth

    re = requests.get(url=enroll_api, headers=headers)
    return re


def main():
    r = get_timetable_by_request()
    print(r)


if __name__ == '__main__':
    main()
