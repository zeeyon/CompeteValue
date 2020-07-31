$(document).ready(function(){
	$("input[type=checkbox]").click(function(){
		check_lists_reload();
	})
	return_color();
});

var ages=[
	{name:'age-10', text:'10대'},
	{name:'age-20', text:'20대'},
	{name:'age-30', text:'30대'}
];

var genders=[
	{name:'gender-male', text:'남성'},
	{name:'gender-female', text:'여성'}
]

var areas=[
	{name:'area-seoul', text:'서울'},
	{name:'area-busan', text:'부산'},
	{name:'area-daegu', text:'대구'},
	{name:'area-gwanju', text:'광주'},
	{name:'area-incheon', text:'인천'},
	{name:'area-daejeon', text:'대전'},
	{name:'area-ulsan', text:'울산'},
	{name:'area-gyeonggi', text:'경기'},
	{name:'area-gangwon', text:'강원'},
	{name:'area-chungcheongbuk', text:'충북'},
	{name:'area-chungcheongnam', text:'충남'},
	{name:'area-jeollabuk', text:'전북'},
	{name:'area-jeollanam', text:'전남'},
	{name:'area-gyeongsangbuk', text:'경북'},
	{name:'area-gyenogsangnam', text:'경남'},
	{name:'area-seoul', text:'세종'},
	{name:'area-jeju', text:'제주'}
]

var fields=[
	{name:'field-web', text:'웹'},
	{name:'field-mobile', text:'모바일'},
	{name:'field-research', text:'연구'},
	{name:'field-ai', text:'인공지능'},
	{name:'field-bigdata', text:'빅데이터'},
	{name:'field-game', text:'게임'},
	{name:'field-embedded/web', text:'임베디드'},
	{name:'field-security', text:'보안'},
	{name:'field-etc', text:'기타'}
]

var all= ages.concat(genders, areas, fields);

function check_lists_reload(){
	for(var i=0; i<check_lists.length; i++)
	$("#check-box-add-li").remove();

	var checked_list=[];
	var i=0;
	$("input[type=checkbox]").each(function(){ 
		if($(this).is(":checked"))  
			checked_list.push(i);
		i++;
	});
	for(var j=0; j<checked_list.length; j++)
		check_lists.push(all[checked_list[j]].text);  
}

var check_lists=[];

var check_list=new Vue({
	delimiters: ['[[', ']]'],
	el:'#check-box-add',
	data:{
		check_list:check_lists
	}
})

function check_box_remove(el){
	var k=0;
	for(var k=0; k<all.length; k++)
		if(all[k].text.concat("X")==el.closest("li").textContent)
			break;

	$("input[type=checkbox]").each(function(){ 
		if(k==0)  
			$(this).prop("checked", false);
		k--;
	});
	check_lists_reload();
}

/**
 * 체크박스
 */

var check_age=new Vue({
	delimiters: ['[[', ']]'],
	el:'#check-box-age',
	data:{
		age:ages
	}
})

var check_gender=new Vue({
	delimiters: ['[[', ']]'],
	el:'#check-box-gender',
	data:{
		gender:genders
	}
})

var check_area=new Vue({
	delimiters: ['[[', ']]'],
	el:'#check-box-area',
	data:{
		area:areas
	}
})

var check_field=new Vue({
	delimiters: ['[[', ']]'],
	el:'#check-box-field',
	data:{
		field:fields
	}
})

/**
 * 글쓰기 박스
 */

var colors = ['#EADFF2', '#DCCBED', '#FEE5EB', '#FCB7D0'];
var post_cards= document.querySelectorAll("#post_card");
var j=0;
function return_color(){
	for(var i=0; i<post_cards.length; i++)
	{
		$(post_cards[i]).find('#post_card_user').css('background-color', colors[j%4]);
		j++;
	}
} 

