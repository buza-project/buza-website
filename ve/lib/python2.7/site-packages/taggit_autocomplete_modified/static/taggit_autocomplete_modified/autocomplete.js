

jQuery().ready(function() {
	jQuery(".autocomplete").each(function () {
		console.log('Autocompleting on ' + $(this).attr('id') + ' to url: ' + $(this).attr('autocomplete-url'));
		$(this).autocomplete($(this).attr('autocomplete-url'), { multiple: true });
	});
});