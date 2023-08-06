#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import re



def validateNickname(name, minLength=2, maxLength=6):
    """
   验证 nickname (中文、字母、数字，下划线)

   :param name: 名字
   :param minLength: 最小长度（默认：2）
   :param maxLength: 最多长度（默认：6）
   :return: bool

   这是一个简单的例子：

   Example
   -------
   >>> validator.validateNickname("李晓明")
   True
   """
    strLen = len(name.encode('utf-8').decode("utf-8"))
    if strLen < minLength or strLen > maxLength:
        return False
    nickname_pattern = re.compile(r'^[0-9a-zA-Z_\u4e00-\u9fa5]*$')
    if nickname_pattern.match(name):
        return True
    else:
        return False


def validateEnNickname(name, minLength=2, maxLength=6):
    """
   验证 nickname (字母、数字，下划线)

   :param name: 名字
   :param minLength: 最小长度（默认：2）
   :param maxLength: 最多长度（默认：6）
   :return: bool

   这是一个简单的例子：

   Example
   -------
   >>> validator.validateEnNickname("Simon_He",minLength=2,maxLength=10)
   True
   """
    strLen = len(name.encode('utf-8').decode("utf-8"))
    if strLen < minLength or strLen > maxLength:
        return False
    nickname_pattern = re.compile(r'^[0-9a-zA-Z_]*$')
    if nickname_pattern.match(name):
        return True
    else:
        return False


def validateChineseName(name):
    """
   验证 中文名字 (中文) 最短两个中文，最长6个中文字符

   :param name: 名字
   :return: bool

   这是一个简单的例子：

   Example
   -------
   >>> validator.validateChineseName("李晓妮")
   True
   """
    chinese_name_pattern = re.compile(r'^[\u4e00-\u9fa5]{2,6}$')
    if chinese_name_pattern.match(name):
        return True
    else:
        return False


def validatePhoneNum(phoneNum):
    """
   验证 手机号码

   :param phoneNum: 电话号码
   :return: bool

   这是一个简单的例子：

   Example
   -------
   >>> validator.validatePhoneNum("18813145200")
   True
   """
    phone_pattern = re.compile(r'^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$')
    if phone_pattern.match(phoneNum):
        return True
    else:
        return False


def validateEmail(email):
    """
   验证 电子邮件

   :param email: 电子邮件
   :return: bool

   这是一个简单的例子：

   Example
   -------
   >>> validator.validateEmail("jackhu@gmail.com")
   True
   """
    email_pattern = re.compile(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$')
    if email_pattern.match(email):
        return True
    else:
        return False


def validateIDCard(idCard):
    """
   校验身份证

   :param idCard: 身份证 15 - 18 位
   :return: bool

   这是一个简单的例子：

   Example
   -------
   >>> validator.validateIDCard("448764199812048827")
   True
   """
    idCard_pattern = re.compile(r'(^[1-9]\d{5}(18|19|([23]\d))\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$)|(^[1-9]\d{5}\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\d{3}$)')
    if idCard_pattern.match(idCard):
        return True
    else:
        return False


def validateLongText(article, minLength=2, maxLength=500):
    """
   验证 文章长度

   :param article: 文章
   :param minLength: 最小长度（默认：2）
   :param maxLength: 最多长度（默认：500）
   :return: bool

   这是一个简单的例子：

   Example
   -------
   >>> validator.validateLongText("飞翔吧，骄傲的海鸥",minLength=2,maxLength=500)
   True
   """
    strLen = len(article.encode('utf-8').decode("utf-8"))
    if strLen < minLength or strLen > maxLength:
        return False
    else:
        return True