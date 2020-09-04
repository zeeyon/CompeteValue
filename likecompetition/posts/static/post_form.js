$("#id_city").change(function() {
	const city_id = $(this).val();
	const url = "cities/" + city_id;

	$.ajax({
		url: url,
		success: function(data) {
			$("#id_area").html(data);
		}
	});
});
