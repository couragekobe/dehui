/*****************************************************地址管理页面js********************************************************/
/**
 * 地址页面添加名称至输入框
 */
$(".sp").click(function () {
	var value = $(this).html();
	$("#addressName").val(value);
})

/**
 * 手机号码中间4位以*号代替转换
 * @param {Object} phone
 */
function changePhone(phone) {
	var dh = phone.replace(/(\d{3})\d{4}(\d{4})/, '$1****$2');
	return dh;
}
/**
 * 校验手机号码格式是否正确
 */
$("#receiverMobile").blur(function () {

	var regex = /^1[3|4|5|8][0-9]\d{4,8}$/;
	var value = $(this).val();
	console.log(value);
	if (!regex.test(value)) {
		alert("手机号码格式不对")
		$('#receiverMobile').val('')
	}
})

/**
 * 提交表单时，校验必填项是否填写完整
 */
$(".save_recipient").click(function () {
	var receiverName = $("#receiverName").val(); // 收件人
	var receiverState = $("#receiverState").val(); // 省
	var receiverCity = $("#receiverCity").val(); // 市
	var receiverDistrict = $("#receiverDistrict").val(); // 区/县
	var receiverAddress = $("#receiverAddress").val(); // 
	var receiverMobile = $("#receiverMobile").val();
	var receiverZip = $("#receiverZip").val();
	var addressName = $("#addressName").val();

	if (receiverName && receiverState && receiverCity && receiverDistrict && receiverAddress && receiverMobile) {
		$.ajax({
			type: 'post',
			url: baseUrl + '/user/addads',
			datatype: JSON,
			data: {"consignee": receiverName,"ads": receiverState + receiverCity + receiverDistrict + receiverAddress,"mobile": receiverMobile,'zipcode': receiverZip,'alias': addressName},
			success: function (response) {
				var result = JSON.parse(response)
				if (result.result) {
					alert('保存信息成功')
					ads(result)
					$('#receiverName').val('')
					$('#receiverAddress').val('')
					$('#receiverMobile').val('')
					$('#receiverZip').val('')
					$('#addressName').val('')
				}
				//绑定默认按钮
				$(".swmr_normal").click(function () {
					setDefault(this);
				})
				//绑定删除事件
				$(".aco_delete").click(function () {
					delAds(this)
				})

			},
			error: function (err) {
				alert('保存失败' + err)
			}
		})
	} else {
		alert("请将必填信息填写完整");
	}
})

/**
 * 地址设为默认点击事件
 */
// $(function(){
// 	$(".swmr_normal").click(function(){
// 		setDefault(this);
// 		console.log(1)
// 	})
// })

/**
 * 设置默认方法
 * @param {Object} e
 */
function setDefault(e) {
	var parent = $(e).parent();
	if ($(parent).siblings().hasClass("aim_active")) {
		$(parent).siblings().removeClass("aim_active");
		$(parent).siblings().children(".dzmc_active").removeClass("dzmc_active").addClass("dzmc_normal");
		$(parent).siblings().children(".swmr_normal").html("设为默认")
		$.ajax({
			type: 'post',
			url: baseUrl + '/user/defads',
			data: {
				adid: $(parent).attr("data-id")
			},
			success: function (response) {
				if (JSON.parse(response).result) {
					alert('设置成功')
				} else if (!JSON.parse(response).result) {
					alert('设置失败' + JSON.parse(response).error)
				}
			},
			error: function (err) {
				alert('设置失败 ' + err)
			}
		})
	}
	$(parent).addClass("aim_active");
	$(parent).children(".dzmc_normal").removeClass("dzmc_normal").addClass("dzmc_active");
	$(e).html("");
}

//删除事件
function delAds(e) {
	var parent = $(e).parent().parent();
	console.log($(parent).attr("data-id"))
	if (confirm("确定删除吗？")) {
		var url = "";
		var param = "";
		$.ajax({
			type: 'get',
			url: baseUrl + '/user/delads',
			data: {
				adid: $(parent).attr("data-id")
			},
			success: function (response) {
				var result = JSON.parse(response)
				if (result.result) {
					alert('删除成功')
					ads(result)
				} else if (!result.result) {
					alert('删除失败' + JSON.parse(response).error)
				}
				//绑定默认按钮
				$(".swmr_normal").click(function () {
					setDefault(this);
				})
				//绑定删除事件
				$(".aco_delete").click(function () {
					delAds(this)
				})
			},
			error: function (err) {
				alert('删除失败' + err)
			}
		})
	}
}
//加载地址列表
function ads(result) {
	var res = JSON.parse(result.data)
	var list =
		"<div class='aim_title'><span class='dzmc dzmc_title'>地址名称</span><span class='dzxm dzxm_title'>姓名</span><span class='dzxq dzxq_title'>地址详情</span><span class='lxdh lxdh_title'>联系电话</span><span class='operation operation_title'>操作</span></div>"
	var defid
	$(res).each(function (index) {
		list += "<div class='aim_content_one' data-id='" + res[index].pk +
			"'>" +
			"<span class='dzmc dzmc_normal'>" + res[index].fields.alias +
			"</span>" +
			"<span class='dzxm dzxm_normal'>" + res[index].fields.consignee +
			"</span>" +
			"<span class='dzxq dzxq_normal'>" + res[index].fields.ads +
			"</span>" +
			"<span class='lxdh lxdh_normal'>" + res[index].fields.mobile +
			"</span>" +
			"<span class='operation operation_normal'><span class='aco_delete'>删除</span></span><span class='swmr swmr_normal'>设为默认</span></div>"
		if (res[index].fields.defaultads) {
			defid = res[index].pk
		}
	})
	list += '</div>'
	$('.address_information_manage').html(list).children('[data-id=' + defid + ']')
		.addClass(
			'aim_active').children("span:first").removeClass('dzmc_normal').addClass(
			'dzmc_active').siblings("span:last").html('')
	$(".lxdh_normal").each(function (i, e) {
		var phone = $(e).html();
		$(e).html(changePhone(phone));
	});
}
/*****************************************************个人信息管理页面js********************************************************/

/**
 * 这是个人信息页面js
 */
// 跳页面
function toPage(page) {
	window.location.href = page;
}


/**
 * 性别选择男
 */
$(".man").click(function () {
	if (!$(".man").hasClass("selected")) {
		$(".man").addClass("selected");
		$(".man img").attr("src", "../images/personage/select.png");
		$(".women").removeClass("selected");
		$(".women img").attr("src", "../images/personage/un_select.png");
		$('.rs_content_sex').attr('data-sex','1')

	}
})

/**
 * 性别选择女
 */
$(".women").click(function () {
	if (!$(".women").hasClass("selected")) {
		$(".women").addClass("selected");
		$(".women img").attr("src", "../images/personage/select.png");
		$(".man").removeClass("selected");
		$(".man img").attr("src", "../images/personage/un_select.png");
		$('.rs_content_sex').attr('data-sex','0')
	}
})
/**
 * 更改用户名，变成可编辑状态
 */
// $(".change_username").click(function () {
// 	var parent = $(".change_username").parent();
// 	$(parent).children(".rs_username").hide();
// 	var name = $(parent).children(".rs_username").html();
// 	$(parent).children(".ed_username").val(name);
// 	$(parent).children(".ed_username").show();
// })

// /**
//  * 更改邮箱，变成可编辑状态
//  */
// $(".change_mail").click(function () {
// 	var parent = $(".change_mail").parent();
// 	$(parent).children(".rs_mail").hide();
// 	var email = $(parent).children(".rs_mail").html();
// 	console.log(email)
// 	$(parent).children(".ed_email").val(email);
// 	$(parent).children(".ed_email").show();
// })