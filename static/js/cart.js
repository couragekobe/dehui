// 单独
function amountadd() {
	var amo = 0;
	$('.Each>span').each(function () {
		if ($(this).hasClass('true')) {
			amo += parseInt($(this).parent().parent().siblings('.totle').children('.totle_information').text());
		}
	});
	$('.susum').text(amo.toFixed(2));
	$('.susumOne').text(amo.toFixed(2));
}
//单条购物项加减
function adddel() {
	//小计和加减
	//加
	$(".add").each(function () {
		$(this).click(function () {
			var $multi = 0;
			var vall = $(this).prev().val();
			vall++;
			$(this).prev().val(vall);
			$multi = (parseInt(vall).toFixed(2) * parseInt($(this).parent().prev().children().eq(1).children().eq(1).text()));
			$(this).parent().next().children().eq(1).text(Math.round($multi).toFixed(2));
			amountadd();
			//商品在购物列表里的id
			var id = $(this).parent().siblings('.pudc').children('.pudc_information').attr('id');
			//商品当前数量
			var num = $(this).prev().val();
			$.ajax({
				type: "get",
				url: baseUrl + "/cart/changecart",
				data: {
					cartid: id,
					single: 0
				},
				success: function (response) {
					var data = JSON.parse(response);
					console.log(data)
				},
				error: function (err) {
					console.log(err)
				}
			});

		})
	});
	//减
	$(".reduc").each(function () {
		$(this).click(function () {
			var id = $(this).parent().siblings('.pudc').children('.pudc_information').attr('id');
			var num = $(this).next().val();
			console.log(num);
			if (num > 1) {
				$.ajax({
					type: "get",
					url: baseUrl + "/cart/changecart",
					data: {
						cartid: id,
						single: 1
					},
					success: function (response) {
						var data = JSON.parse(response);
						console.log(data);
					},
					error: function (err) {
						console.log(err)
					}
				}).then(() => {
					var $multi1 = 0;
					var vall1 = $(this).next().val();
					vall1--;
					if (vall1 <= 0) {
						vall1 = 1;
					}
					$(this).next().val(vall1);
					$multi1 = parseInt(vall1) * parseInt($(this).parent().prev().children().eq(1).children().eq(1).text());
					$(this).parent().next().children().eq(1).text(Math.round($multi1).toFixed(2));
					amountadd();
				})
			}


		})
	})
}
//请求购物车列表成功后的一系列绑定事件
//(删除事件，点击加号向后台发送请求等)
function afterSuccess() {

	if (!$(".imfor")) {
		$('#section').hide();
		$('.none').show();
	}

	// adddel(); //不要重复使用
	$('.imfor').each(function () {
		var price = parseFloat($(this).children('.pices').children('.pices_information').children('span').html());
		var amount = parseFloat($(this).children('.num').children('input').val());
		var amountPrice = price * amount;
		$(this).children('.totle').children('.totle_information').html(amountPrice.toFixed(2));
	});
	//全选
	$(".all").click(function () {
		amountadd();
		if ($('.all>span').hasClass('normal')) {
			$('.all>span').addClass('true').removeClass('normal');
			$('.all>span>img').attr('src', '../images/cart/product_true.png');
			$(".Each>span").each(function () {
				$(this).addClass('true').removeClass('normal');
				$(this).children('img').attr('src', '../images/cart/product_true.png');
			})

			totl();
		} else {
			$('.all>span').addClass('normal').removeClass('true');
			$('.all>span>img').attr('src', '../images/cart/product_normal.png');
			$('.Each>span').addClass('normal').removeClass('true');
			$('.Each>span>img').attr('src', '../images/cart/product_normal.png');
			$(".susum").text(0.00);
			$(".susumOne").text(0.00);
			$('.total').text(0);
			$('.totalOne').text(0);
		}
	})
	//单选
	$('.Each>span').click(function () {
		amountadd();
		$('.all>span').addClass('normal').removeClass('true');
		$('.all>span>img').attr('src', '../images/cart/product_normal.png');
		if ($(this).hasClass('normal')) {
			$(this).addClass('true').removeClass('normal');
			$(this).children('img').attr('src', '../images/cart/product_true.png');
			var amou = parseInt($('.total').text());
			amou++;
			$('.total').text(amou);
			$('.totalOne').text(amou);
			amountadd();
		} else {
			$(this).addClass('normal').removeClass('true');
			$(this).children('img').attr('src', '../images/cart/product_normal.png');
			var amou = parseInt($('.total').text());
			amou--;
			$('.total').text(amou);
			$('.totalOne').text(amou);
			var newamo = parseInt($('.susum').text()) - parseInt($(this).parent().parent().siblings('.totle').children('.totle_information').text());
			$('.susum').text(newamo.toFixed(2));
			$('.susumOne').text(newamo.toFixed(2));
		}
	})
	//删除当前行
	$('.del_d').click(function () {
		var id = $(this).parent().siblings('.pudc').children('.pudc_information').attr('id');
		console.log(id);
		$('.modal').fadeIn();
		$('.no').click(function () {
			$('.modal').fadeOut();
		});
		$('.yes').click(function () {
			// var url = '/delCartItem.html?itemId=' + id;
			// window.location.href = url;

			// $.ajax({
			// 	type: 'get',
			// 	url: baseUrl + '/cart/deletecart',
			// 	data: {
			// 		cartid: id
			// 	},
			// 	success: function (response) {
			// 		var data = JSON.parse(response)
			// 		console.log(data);
			// 		window.location.reload();
			// 	},
			// 	error: function (err) {
			// 		console.log(err)
			// 	}
			// })
		})
	});

	//批量删除
	$(".foot_del").click(function () {
		var str = [];
		$('.Each>span').each(function () {
			if ($(this).hasClass('true')) {
				var id = $(this).parent().parent().next().children('.pudc_information').attr('id');
				str.push(parseInt(id));;
			}
		});
		console.log(str);
		if (str.length > 0) {
			$('.modal').fadeIn();
			$('.no').click(function () {
				$('.modal').fadeOut();
			});
			$('.yes').click(function () {
				// $.ajax({
				// 	type: 'get',
				// 	url: baseUrl + '/cart/deletecart',
				// 	data: {
				// 		cartid: str.toString()
				// 	},
				// 	success: function (response) {
				// 		var data = JSON.parse(response)
				// 		console.log(data);
				// 		window.location.reload();
				// 	},
				// 	error: function (err) {
				// 		console.log(err)
				// 	}
				// })
			});
		} else {
			$('.modalNo').fadeIn();
			$('.close').click(function () {
				$('.modalNo').fadeOut();
			})
		}
	})

}

//请求购物车列表的ajax
// $(function () {
// 	$.ajax({
// 		type: "get",
// 		url: baseUrl + '/cart/cartlist',
// 		success: function (response) {
// 			var data = JSON.parse(response).data;
// 			console.log(data);
// 			var cartListHTML = "";
// 			if (data.length) {
// 				for (var item of data) {
// 					cartListHTML += `
// 				<div class="imfor">
// 					<div class="check">
// 						<div class="Each">
// 							<span class="normal">
// 								<img src="../images/cart/product_normal.png" alt="" />
// 							</span>
// 							<input type="hidden" name="" value="">
// 						</div>
// 					</div>
// 					<div class="pudc">
// 						<div class="pudc_information" id="${item.cartid}">
// 							<img style="width:84px;height:84px;" src="${baseUrl+'/images'+ item.img}" class="lf" />
// 							<input type="hidden" name="" value="">
// 							<span class="des lf">
// 								<a href="product_details.html?goodid=${item.goodid}">${item.title}</a>
// 								<input type="hidden" name="" value="">
// 							</span>
// 							<p class="col lf">
// 								<span>颜色：</span>
// 								<span class="color_des">${item.color} <input type="hidden" name="" value=""></span>
// 								<br>
// 								<span>规格：</span>
// 								<span class="color_des">${item.spec} <input type="hidden" name="" value=""></span>
// 							</p>
//
// 						</div>
// 					</div>
// 					<div class="pices">
// 						<p class="pices_des">皮粉专享价</p>
// 						<p class="pices_information">
// 							<b>￥</b>
// 							<span>${parseFloat(item.price).toFixed(2)}
// 								<input type="hidden" name="" value="">
// 							</span>
// 						</p>
// 					</div>
// 					<div class="num">
// 						<span class="reduc">&nbsp;-&nbsp;</span>
// 						<input type="text" value="${item.amount}" readOnly>
// 						<span class="add">&nbsp;+&nbsp;</span>
// 					</div>
// 					<div class="totle">
// 						<span>￥</span>
// 						<span class="totle_information">${parseFloat(item.price).toFixed(2) * item.amount}</span>
// 					</div>
// 					<div class="del">
// 						<!-- <div>
// 							<img src="img/true.png" alt=""/>
// 							<span>已移入收藏夹</span>
// 						</div>
// 						<a href="javascript:;" class="del_yr">移入收藏夹</a> -->
// 						<a href="javascript:;" class="del_d">删除</a>
// 					</div>
// 				</div>
// 				`
// 				}
// 			}else{
// 				cartListHTML+=`<div class="none"">
// 				<p class="none_title">购物车</p>
// 				<div class="none_top"></div>
// 				<div class="none_content">
// 					<img src="../images/myOrder/myOrder3.png" alt="" class="lf" />
// 					<p class="lf">您的购物车竟然还是空哒( ⊙ o ⊙ )</p>
// 					<span class="lf">赶快去下单吧！</span>
// 					<a href="index.html" class="lf">去购物>></a>
// 				</div>
//
// 			</div>`
// 			}
// 			$("#content_box").append(cartListHTML);
// 		},
// 		error: function (err) {
// 			console.log(err);
// 		}
// 	}).then(() => {
// 		amountadd();
// 		adddel();
// 		afterSuccess();
// 	})
// })

//合计
function totl() {
	var sum = 0.00;
	var amount = 0;
	$(".totle_information").each(function () {
		sum += parseInt($(this).text());
		$(".susum").text(sum.toFixed(2));
		$(".susumOne").text(sum.toFixed(2));
		amount++;
		$('.total').text(amount);
		$('.totalOne').text(amount);
	})
}


//去结算
var itemIds = [];
var totalPrice = 0;
$('.foot_cash').click(function () {
	$('.Each>span').each(function () {
		if ($(this).hasClass('true')) {
			var id = $(this).parent().parent().next().children('.pudc_information').attr('id');
			var num = $(this).parent().parent().siblings('.num').children('input').val();
			//str.push(id);
			itemIds.push({
				id: id,
				amount: num
			})
		}

	});
	totalPrice = $('.susumOne').html();
	console.log(totalPrice);
	console.log(itemIds);
	// if (itemIds.length > 0) {
	// 	localStorage.setItem('itemIds', JSON.stringify(itemIds))
	// 	window.location.href = 'orderConfirm.html';
	// } else {
	// 	// $('.modalBalance').fadeIn();
	// 	// $('.close').click(function () {
	// 	// 	$('.modalBalance').fadeOut();
	// 	// })
	// 	alert('请选择商品')
	window.location.href = '/cart/settlement';


})