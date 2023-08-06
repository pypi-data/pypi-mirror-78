# Installation
    
    pip install PyValidationTool

# Import

    from PyValidationTool import validator
    
# Usage
*  validator.validateChineseName(name)   
> 验证 中文名字 (中文) 最短两个中文，最长6个中文字符
    
    >>> validator.validateChineseName("李晓妮")
    True
    
*  validator.validateEnNickname(name, minLength=2, maxLength=6) 
> 验证 nickname (字母、数字，下划线)
    
    >>> validator.validateEnNickname("Simon_He",minLength=2,maxLength=10)
    True
    
*  validator.validateNickname(name, minLength=2, maxLength=6)
> 验证 nickname (中文、字母、数字，下划线)
    
    >>> validator.validateNickname("李晓明")
    True
    
*  validator.validateIDCard(idCard)
> 校验身份证
    
    >>> validator.validateIDCard("448764199812048827")
    True
    
*  validator.validateLongText(article, minLength=2, maxLength=500)
> 验证文章长度
    
    >>> validator.validateLongText("飞翔吧，骄傲的海鸥",minLength=2,maxLength=500)
    True
    
*  validator.validateEmail(email)   
> 验证 电子邮件
    
    >>> validator.validateEmail("jackhu@gmail.com")
    True
    
*  validator.validatePhoneNum(phoneNum)
> 验证 手机号码
    
    >>> validator.validatePhoneNum("18813145200")
    True
    