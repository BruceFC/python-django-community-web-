$(function(){
	/*主页的搜索栏变化*/
	var $searchtxt = $('#search-text'),
	$search = $('.search'),
	$searchcontent = $('.search-content');
	$searchtxt.on('focusin',function(){
		$search.css('background','#DDE1E6');
		$searchcontent.animate({'width':320},300);
	});
	$searchtxt.on('focusout',function(){
		$search.css('background','#ECEEF1');
		$searchcontent.animate({'width':180},300);
	});
	
	/*回答问题的打开和收起*/
	var $anspro = $('.question .push'),
	$ansBtn = $('.ans-btn'),
	flag = 0;
	$ansBtn.on('click',function(){
		if($(this).attr('flag') == 0){
			$anspro.stop().slideDown();
			flag = 1;
		}else{
			$anspro.stop().slideUp();
			flag = 0;
		}
		$(this).attr('flag',flag);
	});
	
	/*评论的打开和收起*/
	var $answer = $('.answer'),
	// $comment = $answer.find('.answer-bottom>span:eq(0)'),
	$commentcontent = $('.comment-content');
	//在评论按钮上加一个flag属性，初始标志位为0，点击一次后变1，再次点击又会变0，如此循环
	$answer.each(function(){
		var $that = $(this);
		$that.find('.answer-bottom>span:eq(0)').on('click',function(){
			var flag = $(this).attr("flag");
			if($(this).attr("flag") == 1){
				$commentcontent.eq($that.index()).slideUp();
				flag = 0;

			}
			if($(this).attr("flag") == 0){
				$commentcontent.eq($that.index()).slideDown();
			    $answer.eq($that.index()).siblings().find('.comment-content').slideUp();
			    flag = 1;
			}
			$(this).attr("flag",flag);
			
		});
	});
	
	/*用户详情页的子菜单*/
	var $people = $('.people'),
	$userinfo = $('.user-info');
	$people.hover(function(){
		$userinfo.show();
	},function(){
		$userinfo.hide();
	});
	$userinfo.hover(function(){
		$userinfo.show();
	},function(){
		$userinfo.hide();
	});
	
	/*用户信息修改页的切换*/
	var $setbtn = $('.setting-btn li'),
	$line = $('.setting s');
	$setbtn.eq(0).on('click',function(){
		$line.animate({'left':20},500);
		$('.info-setting').show();
		// $('.pass-setting').hide();
	});
	$setbtn.eq(1).on('click',function(){
		$line.animate({'left':140},500);
		// $('.info-setting').hide();
		$('.pass-setting').show();
	});
	
	/*修改头像*/
	var $newphoto = $('.new-photo'),
	$hover = $('.hover');
	$newphoto.hover(function(){
		$hover.stop().show(500);
	},function(){
		$hover.stop().hide(300);
	});
	
	/*检测输入了多少文字*/
	var $textarea = $('.quiz-content textarea'),
	$textnum = $('.text-num');
	$textarea.on('keyup',function(){
		$textnum.html($textarea.val().length);
	});
});
    /*通过location对象传值给另一个页面，在另一个页面做出操作*/
    // function jump1(){
    //         window.location.href="login.html?login-content";
    //         return false;
    //     }
    // function jump2(){
    //         window.location.href="login.html?register-content";
    //         return false;
    // }
