function genFeatureModal (idw, idf) {
    cleanModal (idw);
    var modal = $(idw);
    modal.find('.modal-title').text('Paramètres');
    modal.find('.modal-body').html('coucou' + idf);

}

function genImportModal (id) {
    cleanModal (id);
    var modal = $(id);
    // Set title
    modal.find('.modal-title').text('Importation');
    // Set body content
    modal.find('.modal-body')
	.append($('<div>')
		.append($('<label>')
			.addClass("control-label")
			.text("Select File")
		       )
		.append($('<input>')
			.attr(
			    {
				id: "ttt",
				type: "file",
				class: "file"
			    }
			)
		       )
	       );
    // Set footer content
    modal.find('.modal-footer')
	.append($('<div>')
		.addClass('modal-footer')
		.append($('<button>')
			.attr(
			    {
				type: "button",
				id:"featurefade-ann-btn",
				class:"btn btn-sm btn-default"
			    }
			)
			.text("Annuler")
		       )
		.append($('<button>')
			.attr(
			    {
				type: "button",
				id: "featurefade-imp-btn",
				class: "btn btn-sm btn-primary"
			    }
			)
			.text("Importer")
		       )
	       );
}

function cleanModal (id) {
    var modal = $(id);
    modal.find('.modal-title').text('Void');
    modal.find('.modal-body').empty();
    modal.find('.modal-footer').empty();
}
