jQuery(document).ready(function($) {
	$('#system-device-test').click(function() {
//		$.get($(this).attr("data-href"), {}, function(data) {
//			$('#alerts').append(data);
//		});
		$.ajax({
			url: $(this).attr("data-href"),
			type: 'GET',
			cache: false,
			timeout: 30000,
			beforeSend: function(data) {
				$("#system-device-test > span").removeClass("glyphicon-log-in").addClass("glyphicon-refresh").addClass("spinning");
				$(this).attr("disabled", "disabled");
			},
			success: function(data) {
				$("#system-device-test > span").removeClass("glyphicon-refresh").removeClass("spinning").addClass("glyphicon-log-in");
				$(this).attr("disabled", "disabled");
				$('#alerts').append(data);
			},
			error: function(data) {
				$("#system-device-test > span").removeClass("glyphicon-refresh").removeClass("spinning").addClass("glyphicon-log-in");
				$(this).attr("disabled", "disabled");
				$('#alerts').append(data);
			},
		});
	});
});
