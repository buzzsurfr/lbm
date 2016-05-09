jQuery(document).ready(function($) {
	jQuery(".table-row-clickable").click(function() {
		window.document.location = $(this).data("href");
	});
});

