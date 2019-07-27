from django.shortcuts import render

# Create your views here.


from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound, Http404
from django.contrib.auth.decorators import login_required  # 用于登陆状态验证


from . import models
from goods.models import GoodsSpecification
import json

@login_required(login_url='/user/login/')
def list_all(request):
    # if not request.user.is_authenticated():
    #     return HttpResponseRedirect('/user/login')

    favorites = models.Favorite.objects.filter(user=request.user)
    for item in favorites:
        a_product = item.spec.goods
        try:
            s = a_product.goods_images
            goods_images = eval(s)
            item.head_image = '/images/goods/' + str(a_product.id) + '/' + goods_images[0]
        except:
            item.head_image = '/images/default.png'  # 没有图片时head_image 置为空字符串
    if favorites:
        goods = models.GoodsSpecification.objects.filter(id=favorites[0].spec.id)
        return render(request, 'favorite/favorite_list.html', locals())
    else:
        return render(request, 'favorite/favorite_list.html', {'ms':'Notdata'})



@login_required(login_url='/user/login/')
def add(request, spec_id):
    # if not request.user.is_authenticated():
    #     return HttpResponseRedirect('/user/login')
    spec = GoodsSpecification.objects.get(id=spec_id)
    a_favorite = models.Favorite(user=request.user, spec=spec)
    a_favorite.save()
    return HttpResponse("success")


def add_ajax(request, spec_id):
    '''用ajax提交收藏（为ajax请求提供接口)
       成功返回: "success"
       失败返回: "failed"
    '''
    json_dict = {"status": 200, "message": "添加成功"}
    if not request.user.is_authenticated():
        json_dict['status'] = 401
        json_dict['message'] = "用户没有登陆"
        return HttpResponse(json.dumps(json_dict))

    try:
        spec = models.Favorite.objects.get(spec_id=spec_id)
        json_dict['message'] = "该商品曾经添加过"
        return HttpResponse(json.dumps(json_dict))
    except:
        pass

    spec = GoodsSpecification.objects.get(id=spec_id)
    a_favorite = models.Favorite(user=request.user, spec=spec)
    a_favorite.save()
    return HttpResponse(json.dumps(json_dict))


@login_required(login_url='/user/login/')
def delete(request, id):
    try:
        a_favorite = models.Favorite.objects.get(id=id)
    except:
        return HttpResponse("删除失败!")

    a_favorite.delete()

    return HttpResponseRedirect("/favorite")


def delete_ajax(request, id):
    '''用ajax提交收藏（为ajax请求提供接口)
       成功返回: "success"
       失败返回: "failed"
    '''
    json_dict = {"status": 200, "message": "删除成功"}
    if not request.user.is_authenticated():
        json_dict['status'] = 401
        json_dict['message'] = "用户没有登陆"
        return HttpResponse(json.dumps(json_dict))
    try:
        a_favorite = models.Favorite.objects.get(id=id)
    except:
        json_dict['status'] = 404
        json_dict['message'] = "没有对应的数据"
        return HttpResponse(json.dumps(json_dict))

    a_favorite.delete()
    return HttpResponse(json.dumps(json_dict))


@login_required(login_url='/user/login/')
def clear_all(request):
    favorites = models.Favorite.objects.all()
    favorites.delete()
    return HttpResponseRedirect("/favorite")
