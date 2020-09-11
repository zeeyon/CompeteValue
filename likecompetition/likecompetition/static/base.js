axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

new Vue({
	el: '#app',
	data: {
		sideBarOpen: false
	}
});
