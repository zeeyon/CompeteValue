var sideBars=[
	{text:'홈', link:"/"},
	{text:'회원가입', link:'/users/signup'},
	{text:'내 정보', link:'/users/mypage'},
	{text:'등록하기', link:'/posts/new'}
];

function toggleMenu(){
	var sideBar=$("#side-bar");
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
