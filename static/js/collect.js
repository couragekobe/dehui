/**
 * Created by ttssiw on 2017/1/3.
 */
//管理收藏夹
$('.manage').click(function () {
    if ($('.manage span').hasClass('normal')) {
        $('.manage span').removeClass('normal').addClass('show');
        $('.manage span').html('取消管理');
        $('.check_top').show();
        $('.mask').show();
    } else {
        $('.manage span').removeClass('show').addClass('normal');
        $('.manage span').html('管理收藏夹');
        $('.check_top').hide();
        $('.mask').hide();
    }
})
// //单选
// $('.mask').click(function(e){
//     if($(this).children().hasClass('maskNormal')){
//         $(this).children().addClass('maskTrue').removeClass('maskNormal');
//         $(this).children().children().attr('src','../images//myCollect/product_true_big.png');
//     }else{
//         $(this).children().addClass('maskNormal').removeClass('maskTrue');
//         $(this).children().children().attr('src','../images/myCollect/product_normal_big.png');
//     }
// })
//全选
$('.all').click(function () {
    if ($('.all span').hasClass('normal')) {
        $('.all>span').addClass('true').removeClass('normal');
        $('.all>span>img').attr('src', '../../images/myCollect/product_true.png');
        $(".mask>div").each(function () {
            $(this).addClass('maskTrue').removeClass('maskNormal');
            $(this).children('img').attr('src', '../../images/myCollect/product_true_big.png');
        })
    } else {
        $('.all>span').addClass('normal').removeClass('true');
        $('.all>span>img').attr('src', '../../images/myCollect/product_normal.png');
        $(".mask>div").each(function () {
            $(this).addClass('maskNormal').removeClass('maskTrue');
            $(this).children('img').attr('src', '../../images/myCollect/product_normal_big.png');
        })
    }
})

$('.del').click(function () {
    var str = [];
    $('.mask>div').each(function () {
        if ($(this).hasClass('maskTrue')) {
            var id = $(this).parent().parent().attr('data-favid');
            str.push(id);
        }
    });
    if (str.length > 0) {
        $('.modal').show();
        //删除宝贝
        $('.yes').click(function () {
            $.ajax({
                type: "post",
                url: baseUrl + "/cart/deletefavorite",
                data: {
                    fids: str
                },
                traditional: true,
                success: function (response) {
                    var result = JSON.parse(response)
                    if (result.result) {
                        $('.modal').hide();
                        alert('删除成功')
                    }
                },
                error: function (err) {
                    console.log(err)
                }
            }).then(() => {
                load()
            })
        })
        $('.no').click(function () {
            $('.modal').hide();
        })
    } else {
        $('.modalNo').fadeIn();
        $('.close').click(function () {
            $('.modalNo').fadeOut();
        })
    }
})
$('.allAdd').click(function () {
    var str = [];
    $('.mask>div').each(function () {
        if ($(this).hasClass('maskTrue')) {
            var goodsid = $(this).parent().parent().attr('data-id');
            var favid = $(this).parent().parent().attr('data-favid');
            str.push({
                goodsid: goodsid,
                favid: favid
            });
        }
    });
    console.log(str);
    if (str.length > 0) {
        $(".modalYi").show();
        $('.yes').click(function () {
            $.ajax({
                type: "POST",
                url: baseUrl + "/cart/favortocart",
                datatype: JSON,
                data: {
                    favor: JSON.stringify(str)
                },
                success: function (response) {
                    var result = JSON.parse(response)
                    console.log(result)
                    if (result.result) {
                        $(".modalYi").hide();
                        alert(result.data)
                    }
                },
                error: function (err) {
                    console.log(err)
                }
            }).then(() => {
                load()
            })
        })
    } else {
        $('.modalAdd').fadeIn();
        $('.close').click(function () {
            $('.modalAdd').fadeOut();
        })
    }
})

// //头部hover
// $(".care").hover(function(){
//     $(this).attr('src',"../images/header/care1.png");
// },function(){
//     $(this).attr('src',"../images/header/care.png");
// });
// $(".order").hover(function(){
//     $(this).attr('src',"../images/header/order1.png");
// },function(){
//     $(this).attr('src',"../images/header/order.png");
// });
// $(".shopcar").hover(function(){
//     $(this).attr('src',"../images/header/shop_car1.png");
// },function(){
//     $(this).attr('src',"../images/header/shop_car.png");
// });


//加入购物车
$(".addCart").click(function () {
    $(".modalYi").show();

})
$('.no').click(function () {
    $('.modalYi').hide();
})