from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound, Http404
import json


from . import models


def goods_list(request, type_id=None):
    '''商品列表
       type_id 为 商品的类型ID号,
           当 URL 为: /goods/list/100/   时, type_id 绑定"100", 
           当 URL 为: /goods/            时, type_id 绑定None
    '''
    if type_id:  # 判断是否有类型id
        try:
            # 根据type_id 找到类型信息
            goods_type = models.GoodsType.objects.get(id=type_id)
            # 根据类型信息找到所有对应的商品存于goods 查询集合中
            goods = models.Goods.objects.filter(goods_type_id=goods_type, is_delete=False, is_saller_empower=True, is_admin_empower=True)
        except:
            # 如果出错, 找到所有符合条件的物品，存于goods中
            goods = models.Goods.objects.filter(is_delete=False, is_saller_empower=True, is_admin_empower=True)
    else:  # 如果没有类型id,找到所有符合条件的物品，存于goods中
        goods = models.Goods.objects.filter(is_delete=False, is_saller_empower=True, is_admin_empower=True)

    # 遍历每一件商品对象
    for a_product in goods:
        # 得到商品信息的全部图片，把第一张图片作用商品的主图(head_image)显示
        s = a_product.goods_images
        goods_images = eval(s)
        try:
            a_product.head_image = "/images/goods/" + str(a_product.id) + "/" +  goods_images[0]
        except IndexError:
            a_product.head_image = '/images/default.png'  #  没有图片时 head_image 置为空字符串

        # 用商品规格的第一个规格的价格作为商品价格, 存在商品对象的price中
        goods_specs = models.GoodsSpecification.objects.filter(goods=a_product)
        try:
            a_product.price = goods_specs[0].price
        except IndexError:
            a_product.price = 9999999999

        
    return render(request, "goods/product_list.html", locals())


def detail(request, goods_id, spec_id=None):
    '''商品详情页
        spec_id 为商品的规格的id,如果有此规格信息时，用spec_id找到相应的商品信息，显示商品(注:spec_id 优先)
        goods_id 为商品的id,当没有spec_id 时，根据此goods_id 来定位唯一个商品
    '''
    try:
        if spec_id:
            a_spec = models.GoodsSpecification.objects.get(id=spec_id)  # 根据规格spec_id找到商品
            a_goods = models.Goods.objects.get(id=a_spec.goods_id)
        else:
            a_goods = models.Goods.objects.get(id=goods_id)  # 根据商品id找到商品
    except:
        raise Http404()  # 没有找到对应的商品，返回 404

    goods_id = a_goods.id  # 修改正goods_id

    # 处理商品基本信息
    title = a_goods.title  # 商品名称
    desc = a_goods.desc  # 商品详细信息
    image_list = eval(a_goods.goods_images)  # 获取主图 head_image
    image_list = ['/images/goods/' + str(a_goods.id) + '/' +img for img in image_list]  # 没图片名添加路径，如"1.png" 改为 "/images/goods/1/1.png"
    if image_list:
        head_image = image_list[0]
    else:
        head_image = '/images/default.png'

    detail_list = eval(a_goods.detail_images)
    goods_type = models.GoodsType.objects.get(id=a_goods.goods_type_id)

    # 处理规格信息
    spec_name = a_goods.spec_name

    goods_specs = models.GoodsSpecification.objects.filter(goods_id=a_goods.id)
    # 以下逻辑来判断当前应当将焦点和价格定位在哪儿个规格上
    if not goods_specs:
        raise Http404("此商品没有对应的规格信息")
    
    if not spec_id:
        spec_id = goods_specs[0].id
    else:
        spec_id = int(spec_id)

    for item in goods_specs:
        if item.id == spec_id:
            item.is_select = True
            price = item.price

    return render(request, "goods/product_details.html", locals())


def search(request):
    return HttpResponse("OK")

