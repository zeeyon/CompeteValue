function toggleMenu(){
	var sideBar=$("#side-bar");
	sideBar.toggleClass('open');
}

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
