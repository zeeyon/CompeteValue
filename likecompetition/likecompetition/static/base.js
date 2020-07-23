
var sideBars=[
	{text:'홈', link:"/1"},
	{text:'회원가입', link:'/accounts/signup/'},
	{text:'내 정보', link:'/users/mypage'},
	{text:'등록하기', link:'/posts/new'}
];

$(document).ready(function(){
	if(window.innerWidth<=960){
		$('.content-main').css('padding-left','10px')
		.css('padding-right','10px');
	}
});

$(window).resize(function(){
	if(window.innerWidth<=960){
		$('.content-main').css('padding-left','10px')
		.css('padding-right','10px');
	}else{
		$('.content-main').css('padding-left','250px')
		.css('padding-right','250px');
	}
}); 

function toggleMenu(){
	var sideBar=$("#side-bar");
	if(sideBar.hasClass("open")){
		sideBar.animate({width:'280px', 'padding-left':'10px', 'padding-right':'10px'},450);
	}else{
		sideBar.animate({width:'0px', 'padding-left':'0px', 'padding-right':'0px'},450);
	}
	sideBar.toggleClass('open');
}

var side_bar=new Vue({
	delimiters: ['[[', ']]'],  
	el:'#side-bar',
	data:{
		sideBar:sideBars
	}
})

var header_menu=new Vue({
	delimiters: ['[[', ']]'],
	el:'#header-menu',
	data:{
		sideBar:sideBars
	}
})


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
