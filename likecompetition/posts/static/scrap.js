Vue.component('scrap', {
	template: `<a class="scrap" href="#" onclick="return false" :class="{ scrapped: this.post.scrapped }" @click="toggle_scrap()"></a>`,
	props: {
		'post': Object
	},
	methods: {
		toggle_scrap: function() {
			axios({
				method: this.post.scrapped ? 'delete' : 'post',
				url: '/posts/' + this.post.id + '/scrap'
			})
			.then(response => {
				this.post.scrapped = !this.post.scrapped;
			})
			.catch(error => {
				console.log(error);
			});
		}
	}
});
