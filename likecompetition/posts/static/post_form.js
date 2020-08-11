
$("#id_city").change(function () {
	const url = $("#areaForm").attr("data-areas-url");
	const cityId = $(this).val();

	$.ajax({
		url: url,
		data: {
			'city_id': cityId
		},
		success: function (data) {
			$("#id_area").html(data);
		}
	});
});
