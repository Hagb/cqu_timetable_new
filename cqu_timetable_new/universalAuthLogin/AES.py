# 2020.12.16
# 统一认证的密码加密算法，给tyrz.py提供登录支持
# 利用pkcs7把密码扩展，base64编码加密后的密码

import base64
# 注：python3 安装 Crypto 是 pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple pycryptodome
from Crypto.Cipher import AES


def pkcs7padding(text):
    """
    明文使用PKCS7填充
    最终调用AES加密方法时，传入的是一个byte数组，要求是16的整数倍，因此需要对明文进行处理
    :param text: 待加密内容(明文)
    :return:
    """
    bs = AES.block_size  # 16
    length = len(text)
    bytes_length = len(bytes(text, encoding='utf-8'))
    # tips：utf-8编码时，英文占1个byte，而中文占3个byte
    padding_size = length if(bytes_length == length) else bytes_length
    padding = bs - padding_size % bs
    # tips：chr(padding)看与其它语言的约定，有的会使用'\0'
    padding_text = chr(padding) * padding
    return text + padding_text


def pkcs7unpadding(text):
    """
    处理使用PKCS7填充过的数据
    :param text: 解密后的字符串
    :return:
    """
    try:
        length = len(text)
        unpadding = ord(text[length-1])
        return text[0:length-unpadding]
    except Exception as e:
        pass


def aes_encode(key, content, iv):
    """
    AES加密
    模式cbc
    填充pkcs7
    :param key: 密钥
    :param content: 加密内容
    :return:
    """
    key_bytes = bytes(key, encoding='utf-8')
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
    # 处理明文，加密要求明文长度为16的整数倍
    content_padding = pkcs7padding(content)
    # 加密
    aes_encode_bytes = cipher.encrypt(bytes(content_padding, encoding='utf-8'))
    # 重新编码为base64，保证所有字符都是可以显示的
    result = str(base64.b64encode(aes_encode_bytes), encoding='utf-8')
    return result


def aes_decode(key, content, iv):
    """
    AES解密
    key,iv使用同一个
    模式cbc
    去填充pkcs7
    :param key:
    :param content:
    :return:
    """
    try:
        key_bytes = bytes(key, encoding='utf-8')
        cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
        # base64解码
        aes_encode_bytes = base64.b64decode(content)
        # 解密
        aes_decode_bytes = cipher.decrypt(aes_encode_bytes)
        # 重新编码
        result = str(aes_decode_bytes, encoding='utf-8')
        # 去除填充内容
        result = pkcs7unpadding(result)
    except Exception as e:
        pass
    if result == None:
        return ""
    else:
        return result


def getPassword(password: str, key: str):
    # 偏移参数，任意16位字符，直接全用A
    iv = bytes("A"*16, encoding='utf-8')
    # 加密内容，任意64位字符后面跟上密码明文
    data = 'A'*64 + password.strip()
    # 三个参数进行加密
    mi = aes_encode(key.strip(), data, iv)
    return mi