axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

axios.get('/users/me')
.then(response => {
	Vue.prototype.$user = response.data;
})
.catch(error => {
	console.log(error);
});

new Vue({
	el: '#app',
	data: {
		sideBarOpen: false
	}
});
