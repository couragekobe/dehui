

def isValidVerifycode(request):
    '''判断用户通过POST提交的 verifycode 的值 与 session.verifycode值是否相同。
    如果相同说明验证通过,返回True，否则返回False
    ''' 
    try:
        verifycode1 = request.POST.get('verifycode')
        verifycode2 = request.session.get("verifycode")
        return verifycode1.lower() == verifycode2.lower()  # 转为小写后比较
    except:
        return False

