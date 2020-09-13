Vue.component('post-filter', {
	template: `<div id="filter-box">
	<div class="filter" v-for="filter in filters">
		<div class="filter-name">{{ filter.text }}</div>
		<div class="filter-options">
			<div class="filter-option" v-for="(option, index) in filter.options">
				<input type="checkbox" :id="option.name" :name="filter.name" :value="option" v-model="check_list">
				<label :for="option.name">{{ option.text }}</label>
			</div>
		</div>
	</div>
	<div class="filter">
		<div class="filter-name">언어</div>
		<div class="filter-options">
			<input type="text" id="lang" name="lang">
		</div>
	</div>
	<div id="check-list">
		<ul>
			<li v-for="option in check_list">
				<span class="option-name">{{ option.text }}</span>
				<span class="remove-option" v-on:click="remove_option(option)">×</span>
			</li>
		</ul>
	</div>
</div>`,
	data: function() {
		return {
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
			page: 1
		}
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
			this.query[0] = '/posts/?page=' + this.page;
			var query_string = this.query.join('&');
			axios.get(query_string)
			.then(response => {
				this.$emit('update-post', response.data);
			})
			.catch(error => {
				console.log(error);
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
		}
	},
	created: function() {
		this.send_query();
	}
});

Vue.component('post-card', {
	template: `<div class="post-card" @click="open_post_detail()">
	<div class="profile">
		<div class="profile-image-box"><img class="profile-image" src="/static/images/post_card_user.png"></div>
		<div class="user-info-box">
			<span class="user-info">{{ post.user.nickname }} / 남성 / 20세</span><br>
			<span class="area">{{ post.area }}</span>
		</div>
	</div>
	<div class="field">{{ post.field }}</div>
	<div class="lang"></div>
	<span class="date">{{ post.date }}</span>
	<div class="icon" v-on:click.stop>
		<a class="message" href="#" onclick=""></a>
		<scrap :post=post></scrap>
	</div>
</div>`,
	props: {
		'post': Object
	},
	methods: {
		open_post_detail: function() {
			this.$emit('open-detail', this.post);
			var func = () => {
				if ($('#post_detail_card').length) {
					$('#post_detail_card').dialog({
						modal: true,
						width: 1000,
						draggable: false,
						resizable: false,
						create: function() {
							$(this).parent().find('.ui-dialog-titlebar').remove();
							$(this).parent().css('position', 'fixed');
							$(this).parent().css('padding', 0);
							$(this).css('padding', 0);
						},
						open: function() {
							window.onpopstate = () => {
								$('#post_detail_card').dialog('close');
							};
							$('.ui-widget-overlay').on('click', () => {
								$('#post_detail_card').dialog('close');
							});

						}
					});
				} else {
					setTimeout(func, 10);
				}
			};
			func();
		}
	}
});

Vue.component('post-list', {
	template: `<div><post-filter @update-post="posts=$event" ref="filter"></post-filter>
	<div id="post-cards">
		<post-card v-for="post in posts.results" :key="post.id" :post=post @open-detail="detail_post=post"></post-card>
		<div class="post-card filling-empty-space"></div>
		<div class="post-card filling-empty-space"></div>
		<div class="post-card filling-empty-space"></div>
	</div>
	<div id="page-btn">
		<a v-if="posts.previous" href="#" onclick="return false" @click="$refs.filter.prev_page()">&#60;Prev</a>
		<a v-if="posts.next" href="#" onclick="return false" @click="$refs.filter.next_page()">Next&#62;</a>
	</div>
	<post-detail-card v-if="detail_post !== null" :_post="detail_post"></post-detail-card></div>`,
	data: function() {
		return {
			posts: {},
			detail_post: null
		}
	}
});
