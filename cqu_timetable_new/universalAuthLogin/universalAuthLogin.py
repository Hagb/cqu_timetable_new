# 提供统一认证的登录服务，返回session对象
# 2020.08.22
# 2020.09.02
# 2020.09.03
# 先通过card.cqu.edu.cn发送帐号密码尝试登录
# 若成功，再登录预设网址
# 返回session对象和登录的post结果res
# 2020.09.24
# 修正运行逻辑，之前的方式太智障了
# 通过在url_authserver中进行登录，如果返回登录成功的页面，则登录成功，返回Session对象s

# 使用方法：
# 向getLoginData函数中传入用户名和密码
# getLoginData函数将尝试登录http://authserver.cqu.edu.cn/authserver/login
# 若成功，getLoginData函数将返回登录的session
# main中的例子为登录成功后转向user.cqu.edu.cn，将会自动进入登录完成后的用户信息界面，返回网页的代码


import requests
from lxml import etree
from .AES import getPassword


# http://authserver.cqu.edu.cn/authserver/custom/js/encrypt/encrypt.wisedu.js
# encryptAES函数获取加密后的密码

def getLoginData(username, password):
    url_authserver = 'http://authserver.cqu.edu.cn/authserver/login'
    s = requests.Session()
    s.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
    }

    # 判断是否需要验证码
    captchaStatus = isNeedCaptcha(username, s)
    if captchaStatus == 'true':
        print("当前帐号需要验证码才能登录，疑似登录次数失败过多，请先手动成功登录一次以取消验证码")
        exit(1)
    elif captchaStatus != 'false':
        print("获取当前帐号的验证码状态失败，请检查")
        exit(1)

    # 尝试登录
    s, res = sendData(s, username, password, url_authserver)
    if res.url == "http://authserver.cqu.edu.cn/authserver/index.do" and '安全退出' in res.text:
        print("登录成功")
        print(res.url)
        print(res.text)
        print(s.cookies)
        # return sendData(s, username, password, url)
        return s
    elif '您提供的用户名或者密码有误' in res.text:
        print("您提供的用户名或者密码有误")
        exit(1)
    else:
        print("未知错误")
        exit(1)


def isNeedCaptcha(username, s):
    """判断当前帐号是否需要验证码登录，
    返回文本的true false，需要在调用的函数中手动判断
    返回类型为  str  !!!
    """
    r = s.get("http://authserver.cqu.edu.cn/authserver/needCaptcha.html?username=" + username)
    return r.text


def sendData(s, username, password, url):
    """向认证地址post帐号密码等信息
    保留了url参数，不写死，
    方便后期认证方式发生变动或者尝试登录其他页面时直接修改url进而继续登录
    """

    try:
        res = s.get(url)
        html = etree.HTML(res.content)
    except Exception:
        print("访问", url, "失败")
        exit(1)

    try:
        lt = html.xpath("//input[@name='lt']/@value")[0]
        dllt = html.xpath("//input[@name='dllt']/@value")[0]
        execution = html.xpath("//input[@name='execution']/@value")[0]
        _eventId = html.xpath("//input[@name='_eventId']/@value")[0]
        rmShown = html.xpath("//input[@name='rmShown']/@value")[0]
        keyRaw: str = html.xpath("script[2]")[0].text
        key = keyRaw[keyRaw.rfind('= ') + 3: keyRaw.rfind('"')]
    except Exception:
        print("从 http://authserver.cqu.edu.cn 获取登录信息发生错误，可能登录方式有所变动")
        exit(1)

    try:
        # 对传入的密码进行加密
        password2 = getPassword(password, key)
    except Exception:
        print("获取加密后的登录密码失败")
        exit(1)

    data = {
        'username': username,
        'password': password2,
        'execution': execution,
        'dllt': dllt,
        '_eventId': _eventId,
        'lt': lt,
        'rmShown': rmShown
    }

    try:
        # print(data)
        res = s.post(url, data=data)
    except Exception:
        print("登录失败")
        exit(1)
    else:
        # print(s.cookies)
        return s, res