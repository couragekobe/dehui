from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from PIL import Image, ImageFont, ImageDraw
import random
import sys

# Create your views here.


def rmdRGB():
    c1 = random.randrange(0, 255)
    c2 = random.randrange(0, 255)
    c3 = random.randrange(0, 255)
    return c1, c2, c3


def verify_code(request):
    bgcolor = '#997679'
    width = 100
    height = 25
    # 创建画布
    im = Image.new('RGB', (width, height), bgcolor)
    # 创建画笔
    draw = ImageDraw.Draw(im)
    # 画点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)

    # 添加干扰线
    for i in range(8):
        x1 = random.randrange(0, width)
        y1 = random.randrange(0, height)
        x2 = random.randrange(0, width)
        y2 = random.randrange(0, height)
        draw.line((x1, y1, x2, y2), fill=rmdRGB())
    # 添加圆

    # 写字
    str1 = '123456789abcdefghijkmnpgrstuvwxyzABCDEFJHJKLMNPQRSTUVWXYZ'
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]

    # 字体
    # font = ImageFont.truetype('/usr/share/fonts/truetype/fonts-japanese-gothic',23)
    # 判断是什么操作系统(操作系统兼容)
    if sys.platform == 'linux':
        font = ImageFont.truetype(
            '/usr/share/fonts/truetype/fonts-japanese-gothic', 23)
    elif sys.platform == 'darwin':  # Mac OS X
        font = ImageFont.truetype('/Library/Fonts/Arial.ttf', 23)
    elif sys.platform == 'win32':
        font = ImageFont.truetype(r'C:\Windows\Fonts\arial.ttf', 23)
    else:
        raise Http404("暂不支持此操作系统: " + sys.platform)

    # 构造字体颜色
    fontcolors = ['yellow', 'blue', 'green', 'red', 'orange', 'pink']

    draw.text((5, 2), rand_str[0], fill=random.sample(fontcolors, 1)[0], font=font)
    draw.text((25, 2), rand_str[1], fill=random.sample(fontcolors, 1)[0], font=font)
    draw.text((45, 2), rand_str[2], fill=random.sample(fontcolors, 1)[0], font=font)
    draw.text((70, 2), rand_str[3], fill=random.sample(fontcolors, 1)[0], font=font)

    # 结束
    del draw
    # 存入session
    request.session['verifycode'] = rand_str
    print('verifycode', request.session['verifycode'])
    # 内存文件操作
    import io
    # 获得一个内存缓存区
    buf = io.BytesIO()
    # 将图片保存在缓存区,格式为png
    im.save(buf, 'png')
    # 将缓存区的内容返回给前端 .getvalue 是把缓存区的所有数据读取
    return HttpResponse(buf.getvalue(), 'image/png')
