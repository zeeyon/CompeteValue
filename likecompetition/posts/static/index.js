var filter_box = new Vue({
	delimiters: ['[[', ']]'],
	el: '#filter-box',
	data: {
		filters: [
			{name_kor:'나이', name_eng:'age', options:[
				{name:'age10', text:'10대'},
				{name:'age20', text:'20대'},
				{name:'age30', text:'30대'}
			]},
			{name_kor:'성별', name_eng:'gender', options:[
				{name:'male', text:'남성'},
				{name:'female', text:'여성'}
			]},
			{name_kor:'지역', name_eng:'area', options:[
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
			{name_kor:'분야', name_eng:'field', options:[
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
		],
		check_list: []
	},
	methods: {
		remove_option: function(option) {
			this.check_list.splice(this.check_list.indexOf(option), 1);
		}
	}
})
