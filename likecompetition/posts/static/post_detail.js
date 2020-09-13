Vue.component('comment-box', {
	template: `<div id="comment_box">
	<div v-for="(comment, idx) in comments" class="comment">
		<div class="profile">
			<img class="profile_img" src="/static/images/post_card_user.png" />
			<span class="nickname">{{ comment.user.nickname }}</span>
			<span class="date">{{ comment.date }}</span>
		</div>
		<div class="content">{{ comment.content }}</div>
		<a v-if="comment.user.id === $user.id" class="delete" href="#" onclick="return false" @click="delete_comment(idx)">삭제하기</a>
	</div>
</div>`,
	props: {
		'comments': Array
	},
	methods: {
		delete_comment: function(idx){
			axios.delete('/posts/comments/' + this.comments[idx].id)
			.then(respone => {
				this.comments.splice(idx, 1);
			})
			.catch(error => {
				console.log(error);
			});
		}
	}
});

Vue.component('comment-form', {
	template: `<form id="comment_form" method="post" onsubmit="return false">
	<img class="profile_img" src="/static/images/post_card_user.png" />
	<textarea name="content" cols="40" rows="10" placeholder="Add a comment..." required id="id_content"></textarea>
	<input type="submit" value="등록" @click="create_comment()" />
</form>`,
	props: {
		'post_id': Number
	},
	methods: {
		create_comment: function(){
			axios.post('/posts/' + this.post_id + '/comments', new FormData(this.$el))
			.then(response => {
				this.$el.reset();
				this.$emit('add_comment', response.data);
			})
			.catch(error => {
				console.log(error);
			});
		}
	}
});

Vue.component('post-detail-card', {
	template: `<div id="post_detail_wrap">
	<div id="post_detail_card" v-if="post !== null">
		<div class="profile">
			<img class="profile_img" src="/static/images/post_card_user.png" /><br>
			<span class="user_info">{{ post.user.nickname }}</span><br>
			<span class="area">{{ post.area }}</span>
		</div>
		<div class="contents">
			<div class="field">{{ post.field }}</div>
			<div class="langs">
				<div class="lang">#테스트</div>
				<div class="lang">#테스트</div>
				<div class="lang">#테스트</div>
			</div>
			<div class="content">{{ post.content }}</div>
			<div class="comment_cnt">
				<template v-if="comments !== null">
					<span>{{ comments.length }} comments</span>
				</template>
				<template v-else>
					<a :href="'/posts/' + post.id + '/detail'">{{ post.comment_cnt }} comments</a>
				</template>
			</div>
		</div>
		<div class="icon">
			<a class="message" href="#"></a>
			<scrap :post=post></scrap>
			<template v-if="post.user.id === $user.id">
			<a class="edit" :href="'/posts/' + post.id + '/edit'"></a>
			<a class="delete" href="#" @click="delete_post()"></a>
			</template>
		</div>
	</div>
	<template v-if="comments !== null">
		<comment-box :comments="comments"></comment-box>
		<comment-form v-if="post !== null" :post_id="post.id" @add_comment="add_comment"></comment-form>
	</template>
</div>`,
	props: {
		'_post': {
			type: Object,
			default: null
		},
		'post_id': {
			type: Number,
			default: null
		},
		'show_comments': {
			type: Boolean,
			default: false
		}
	},
	data: function() {
		return {
			comments: null,
			post: this._post
		}
	},
	methods: {
		delete_post: function() {
			axios.delete('/posts/' + this.post.id)
			.then(response => {
				location.href = '/';
			})
			.catch(error => {
				console.log(error);
			});
		},
		add_comment: function(val) {
			axios.get('/posts/comments/' + val)
			.then(response => {
				this.comments.push(response.data);
			})
			.catch(error => {
				console.log(error);
			});
		}
	},
	watch: {
		_post: function() {
			this.post = this._post;
		}
	},
	created: function() {
		if (this.post === null) {
			axios.get('/posts/' + this.post_id)
			.then(response => {
				this.post = response.data;
			})
			.catch(error => {
				console.log(error);
			});
		}
		if (this.show_comments) {
			axios.get('/posts/' + this.post_id + '/comments')
			.then(response => {
				this.comments = response.data.results;
			})
			.catch(error => {
				console.log(error);
			});
		}
	}
});
