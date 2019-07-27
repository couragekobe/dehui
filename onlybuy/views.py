from django.http import HttpResponse, HttpResponseRedirect  # 导入响应类
from django.shortcuts import render



def homepage(request):
    print("homepage is called")
    # return HttpResponse("首页")
    return render(request, 'index.html')

def header(request):
    return render(request, "header.html")

def footer(request):
    return render(request, "footer.html")

