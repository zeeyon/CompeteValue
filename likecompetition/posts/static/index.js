
var scrap = {
	template: '<a class="scrap" v-bind:class="{ scrapped: this.isScrapped }" href="#" onclick="return false" v-on:click="toggle_scrap()"></a>',
	props: {
		id: Number,
		initialScrapped: Boolean
	},
	data: function() {
		return {
			isScrapped: this.initialScrapped
		}
	},
	methods: {
		toggle_scrap: function() {
			var vue = this;
			var method = this.isScrapped ? 'delete' : 'post';
			axios({
				method: method,
				url: '/posts/' + this.id + '/scrap'
			})
			.then(function(response) {
				vue.isScrapped = !vue.isScrapped;
			})
			.catch(function(error) {
				console.log(error);
			});
		}
	}
};

new Vue({
	delimiters: ['[[', ']]'],
	el: '#index',
	components: {
		'scrap': scrap,
	},
	data: {
		filters: [
			{name:'age', text:'나이', options:[
				{name:'10s', text:'10대'},
				{name:'20s', text:'20대'},
				{name:'30s', text:'30대'}
			]},
			{name:'gender', text:'성별', options:[
				{name:'male', text:'남성'},
				{name:'female', text:'여성'}
			]},
			{name:'area', text:'지역', options:[
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
			{name:'field', text:'분야', options:[
				{name:'web', text:'웹'},
				{name:'android', text:'안드로이드'},
				{name:'ios', text:'iOS'},
				{name:'game', text:'게임'},
				{name:'ml', text:'머신러닝'},
				{name:'bigdata', text:'빅데이터'},
				{name:'iot', text:'IoT'},
				{name:'blockchain', text:'블록체인'},
				{name:'vr', text:'가상현실'},
				{name:'etc', text:'기타'}
			]}
		],
		check_list: [],
		query: ['?page=1'],
		page: 1,
		posts: null
	},
	methods: {
		remove_option: function(option) {
			this.check_list.splice(this.check_list.indexOf(option), 1);
		},
		next_page: function() {
			window.scrollTo(0, 0);
			this.page++;
			this.send_query();
		},
		prev_page: function() {
			window.scrollTo(0, 0);
			this.page = Math.max(this.page - 1, 1);
			this.send_query();
		},
		send_query: function() {
			var vue = this;
			this.query[0] = '/posts/?page=' + this.page;
			var query_string = this.query.join('&');
			axios.get(query_string)
			.then(function(response) {
				vue.posts = response.data;
			})
			.catch(function(error) {
				console.log(error);
			});
		},
		open_post_detail: function(post_id) {
			var url= document.getElementById(post_id).href;
			var now_href= window.location.href;
			history.pushState(null, null, url);
			$("#dialog").load(url.concat(" .post_detail_box"));
			$("#dialog").dialog({
				modal: true,
				width: '1000',
				height: 'auto',
				draggable: false,
				resizable:false,
				open:function(){
					$(this).parents(".ui-dialog:first").find(".ui-dialog-titlebar").remove();
					window.onpopstate = () => {
						$('#dialog').dialog('close');
					};
					$('.ui-widget-overlay').on('click', function(){ $('#dialog').dialog('close');})
					$('.ui-dialog').css("padding", "0");
					$('.ui-dialog-content').css("padding", "0");
				},
				close:function(){
					history.pushState(null, null, now_href);
				}
			});
		}
	},
	watch: {
		check_list: function() {
			this.query.splice(1, this.query.length - 1);
			for (var i = 0; i < this.filters.length; i++) {
				for (var j = 0; j < this.filters[i].options.length; j++) {
					if (this.check_list.includes(this.filters[i].options[j])) {
						this.query.push(this.filters[i].name + '=' + this.filters[i].options[j].name);
					}
				}
			}
			this.page = 1;
			this.send_query();
		},
	},
	created: function() {
		this.send_query();
	}
});

