#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   PyValidationTool.py
@Time    :   2020/9/5
@Author  :   SimonHe
@Version :   0.1.0
@Contact :   simonheusing@gmail.com
@License :   (C)Copyright 2020-2022
@Desc    :   None
'''
import re
SENSITIVE_WORDS = ("你老母",)

def replace(text):
    return re.sub("|".join(SENSITIVE_WORDS), "***", text)
