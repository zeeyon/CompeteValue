
$(window).scroll(function(event){ 
	var scrollLocation=$('html').scrollTop();
	$('header').css('background-color','rgba(28, 28, 28, '+Math.min(1, scrollLocation*0.003)+')');
});

$(document).ready(function(){
/* 	$('#card-input').on('keyup', function(){
		if($('#card-input').val().length>100){
			alert("100글자를 초과할 수 없습니다.");
			$('#card-input').val($(this).val().substring(0, 100));
		}
	}); */
	$('header').css('background-color','rgba(28, 28, 28, 0)');
});

function modifyMode(){
	$('.modify').toggleClass('hide');
	$('.modify').toggleClass('modify-background');
	$('#menu-btn-modify').toggleClass('modify-mode');
}
function writeMode(){
	$('.newcard').toggleClass('popup');
	$('.newcard').toggleClass('hide');
}

function deleteCard(){
	alert("delete");
}
function modifyCard(){
	alert("modify");
}/* 
function closePopup(t){
	if($('#card-input').val()==''){
		t.classList.remove('popup');
		t.classList.add('hide');
		return 0;
	}
	//if(confirm("입력을 취소하시겠습니까?")){
		t.classList.remove('popup');
		t.classList.add('hide');
	//}
} */

function cropImage(){
	window.name="이미지 자르기";
	var popup = window.open("image_crop.html", "crop", "width=603px, height=670px, resizable=no, scrollbars=no");
		
	var input=document.getElementById("user_profile_img");
	var fReader=new FileReader();
	fReader.readAsDataURL(input.files[0]);
	fReader.onloadend=function(e){
		document.getElementById("imgName").value=e.target.result;
	}
}