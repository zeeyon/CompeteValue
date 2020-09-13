axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

async function getUser() {
	try {
		var response = await axios.get('/users/me');
		Vue.prototype.$user = response.data;
	} catch (error) {
		console.log(error);
	}
}
getUser();

new Vue({
	el: '#app',
	data: {
		sideBarOpen: false
	}
});
