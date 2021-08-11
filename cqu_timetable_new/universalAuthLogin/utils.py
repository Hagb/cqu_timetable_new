# 2020年12月21日 01:39:41
# 基于tryz.py登录新的选课网站http://my.cqu.edu.cn/enroll/Home
# 目前可返回课表json

import json
import requests
import urllib.parse
from .universalAuthLogin import getLoginData


def getAccessTokenDict(s: requests.Session) -> dict:
    '''
    传入统一认证登录后的session，返回选课系统登录后的 Authorization 字典作为 headers 给其他接口调用
    实现思路：先去token_index里获取重定向后的页面url，获取url中的code参数
    借助code参数从token网站中得到access_token
    '''
    s.get('http://authserver.cqu.edu.cn/authserver/login?service=http://my.cqu.edu.cn/authserver/authentication/cas')
    token_index = 'http://my.cqu.edu.cn/authserver/oauth/authorize?client_id=enroll-prod&response_type=code&scope=all&state=&redirect_uri=http%3A%2F%2Fmy.cqu.edu.cn%2Fenroll%2Ftoken-index'
    temp = s.get(token_index)
    urlParse = urllib.parse.urlparse(temp.url)
    # print(temp.cookies)
    try:
        code = urllib.parse.parse_qs(urlParse.query)['code'][0]
        print(code)
    except:
        print('在获取token的路上获取code参数时遇到了问题')
        exit(1)

    data = {
        "client_id": "enroll-prod",
        "client_secret": "app-a-1234",
        "code": code,
        "redirect_uri": "http://my.cqu.edu.cn/enroll/token-index",  # data里面的参数不要转义
        "grant_type": "authorization_code",
    }
    r = s.post('http://my.cqu.edu.cn/authserver/oauth/token', data,
               headers={"Authorization": "Basic ZW5yb2xsLXByb2Q6YXBwLWEtMTIzNA=="})
    access_token = r.json()['access_token']
    token_type = r.json()['token_type']
    return {"Authorization": token_type+" "+access_token}


def getStuInfoJson(s: requests.Session, header) -> json:
    # 学生信息
    r = s.get('http://my.cqu.edu.cn/authserver/simple-user',
              headers=header)  # 后面记得都得加这个
    return r.json()


def getStrId(j: json) -> str:
    # 返回学号
    return j['code']


def getClassJson(s: requests.Session, header, stuId='') -> json:
    # 课表json
    if stuId == '':
        stuId = getStrId(getStuInfoJson(s, header))
    r = requests.get('http://my.cqu.edu.cn/enroll-api/timetable/student/' + stuId,
              headers=header)  # 后面记得都得加这个
    return r.json()


def getScoreJson(header) -> json:
    r = requests.get('http://my.cqu.edu.cn/sam-api/score/student/score',
              headers=header)  # 后面记得都得加这个
    return r.json()