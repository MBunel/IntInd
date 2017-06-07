"use strict";

const bodycont = [
    {
	'type':'<div>',
	'childs':[
	    {
		'type':'<label>',
		'childs':[],
		'attr': {}
	    },
	    {
		'type':'<input>',
		'childs':[],
		'attr': {
		    'type':'email',
		    class: 'form-control'}
	    }
	],
	attr:{'class': 'form-group'}},
    {
	'type':'<div>',
	'childs':[
	    {
		'type':'<label>',
		'childs':[],
		'attr': {}
	    },
	    {
		'type':'<input>',
		'childs':[],
		'attr': {
		    'type':'email',
		    class: 'form-control'
		}
	    }
	],
	attr:{'class': 'form-group'}},
    {
	'type':'<div>',
	'childs':[
	    {
		'type':'<label>',
		'childs':[],
		'attr': {}
	    },
	    {		'type':'<input>',
		'childs':[],
		'attr': {
		    'type':'email',
		    class: 'form-control'
		}
	    }
	],
	attr:{'class': 'form-group'}
    }
];

function genFeatureModal (idw, idf) {
    cleanModal (idw);
    var modal = $(idw);
    modal.find('.modal-title').text('Noeud ' + idf);

    modal.find('.modal-body')

	.append($('<div>')
		.addClass('btn-group')
		.attr('data-toogle', 'buttons')
		.append($('<button>')
			. addClass('btn btn-primary')
		       )
		.append($('<button>')
			. addClass('btn btn-primary')
		       )
		.append($('<button>')
			. addClass('btn btn-primary')
		       )
		.append($('<button>')
			. addClass('btn btn-primary')
		       )
	       )

	.append($('<from>')

		.append($('<div>')
	    		.addClass('form-group')
	    		.append($('<label>')
	    			.text("Champ1"))
	    		.append($('<input>')
	    			.addClass('form-control')
	    			.attr('type', 'email')
	    		       )
	    	       )
	       );





    modal.find('.modal-footer')
	.append($('<div>')
		.append($('<button>')
			.attr(
			    {
				type: "button",
				id:"featurefade-ann-btn",
				class:"btn btn-sm btn-default"
			    }
			)
			.on('click',
			    function(){
				$("#GenericModal").modal("hide");
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
			.on('click',
			    function() {
				// mise à jour des données du marqueur
				updateMarkerData(idf, {'hop': 'hep', 'non':'si'});
				// supp fen
				$("#GenericModal").modal("hide");
			    }
			   )
			.text("Valider")
		       )
	       );
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
