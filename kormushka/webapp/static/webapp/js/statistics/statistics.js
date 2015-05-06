$(document).ready(function () {
	$('#statistics-tab a').click(function (e) {
		e.preventDefault()
		$(this).tab('show')
	})
})