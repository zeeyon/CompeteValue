var sideBars=[
	{text:'홈', link:"/1"},
	{text:'글쓰기', link:'/posts/new'} 
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
