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
    cleanModal(idw);
    var modal = $(idw);
    var defIdfVal = markersGroup._layers[idf].options;
    // Windows title
    modal.find('.modal-title').text('Noeud ' + idf);
    // Windows content
    modal.find('.modal-body')
	.append($('<from>')
		.append($('<div>')
	    		.addClass('form-group')
	    		.append($('<label>')
	    			.text("Q"))
	    		.append($('<input>')
	    			.addClass('form-control')
	    			.attr({
				    'id': 'Qinput',
				    'type': 'email',
				    'value': defIdfVal.Q
				    })
	    		       )
	    	       )
		.append($('<div>')
	    		.addClass('form-group')
	    		.append($('<label>')
	    			.text("R"))
	    		.append($('<input>')
	    			.addClass('form-control')
	    			.attr({
				    'id': 'Rinput',
				    'type': 'email',
				    'value': defIdfVal.R
				})
	    		       )
	    	       )
		.append($('<div>')
	    		.addClass('form-group')
	    		.append($('<label>')
	    			.text("C"))
	    		.append($('<input>')
	    			.addClass('form-control')
	    			.attr({
				    'id': 'Cinput',
				    'type': 'email',
				    'value': defIdfVal.C
				})
	    		       )
	    	       )
		.append($('<div>')
	    		.addClass('form-group')
	    		.append($('<label>')
	    			.text("P"))
	    		.append($('<input>')
	    			.addClass('form-control')
	    			.attr({
				    'id': 'Pinput',
				    'type': 'email',
				    'value': defIdfVal.P
				})
	    		       )
	    	       )
		.append($('<div>')
	    		.addClass('form-group')
	    		.append($('<label>')
	    			.text("B"))
	    		.append($('<input>')
	    			.addClass('form-control')
	    			.attr({
				    'id': 'Binput',
				    'type': 'email',
				    'value': defIdfVal.B
				})
	    		       )
	    	       )
	       );
    // Windows footer
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
				updateMarkerData(idf, {
				    'Q': modal.find('#Qinput').val(),
				    'R': modal.find('#Rinput').val(),
				    'C': modal.find('#Cinput').val(),
				    'P': modal.find('#Pinput').val(),
				    'B': modal.find('#Binput').val()
				});
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
