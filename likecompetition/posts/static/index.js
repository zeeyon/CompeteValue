$(document).ready(function(){
	$("input[type=checkbox]").click(function(){
		check_lists_reload();
	})
});

var all=null;
var check_lists=[];

/**
 * 체크박스
 */
 var check_box=new Vue({
	delimiters: ['[[', ']]'],
	el:'#check-box',
	data:{
		qwerty:[
			{name_kor:'나이', name_eng:'age', elems:[
				{name:'age10', text:'10대'},
				{name:'age20', text:'20대'},
				{name:'age30', text:'30대'}
			]},
			{name_kor:'성별', name_eng:'gender', elems:[
				{name:'male', text:'남성'},
				{name:'female', text:'여성'}
			]},
			{name_kor:'지역', name_eng:'area', elems:[
				{name:'seoul', text:'서울'},
				{name:'busan', text:'부산'},
				{name:'daegu', text:'대구'},
				{name:'incheon', text:'인천'},
				{name:'gwangju', text:'광주'},
				{name:'daejeon', text:'대전'},
				{name:'ulsan', text:'울산'},
				{name:'sejong', text:'세종'},
				{name:'gyeonggi', text:'경기'},
				{name:'gangwon', text:'강원'},
				{name:'chungbuk', text:'충북'},
				{name:'chungnam', text:'충남'},
				{name:'jeonbuk', text:'전북'},
				{name:'jeonnam', text:'전남'},
				{name:'gyeongbuk', text:'경북'},
				{name:'gyenognam', text:'경남'},
				{name:'jeju', text:'제주'}
			]},
			{name_kor:'분야', name_eng:'field', elems:[
				{name:'web', text:'웹'},
				{name:'mobile', text:'모바일'},
				{name:'research', text:'연구'},
				{name:'ai', text:'인공지능'},
				{name:'bigdata', text:'빅데이터'},
				{name:'game', text:'게임'},
				{name:'embedded', text:'임베디드'},
				{name:'security', text:'보안'},
				{name:'etc', text:'기타'}
			]}
		]
	}
 })

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
