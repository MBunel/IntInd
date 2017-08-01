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
		.addClass('form-horizontal')
		.append($('<div>')
	    		.addClass('form-group')
	    		.append($('<label>')
				.attr('for', "Qinput")
				.addClass('col-sm-4 control-label')
	    			.text("Effectif des quotidiens")
			       )
			.append($('<div>')
				.addClass('col-sm-8')
	    			.append($('<input>')
	    				.addClass('form-control')
	    				.attr({
					    'id': 'Qinput',
					    'type': 'email',
					    'placeholder': 'Effectif de Q',
					    'value': defIdfVal.Q
					})
	    			       )
			       )

	    	       )
		.append($('<div>')
	    		.addClass('form-group')
	    		.append($('<label>')
				.attr('for', "Rinput")
				.addClass('col-sm-4 control-label')
	    			.text("Effectif des réflexes")
			       )
			.append($('<div>')
				.addClass('col-sm-8')
	    			.append($('<input>')
	    				.addClass('form-control')
	    				.attr({
					    'id': 'Rinput',
					    'type': 'email',
					    'placeholder': 'Effectif de R',
					    'value': defIdfVal.R
					})
	    			       )
			       )
	    	       )
		.append($('<div>')
	    		.addClass('form-group')
	    		.append($('<label>')
				.attr('for', "Cinput")
				.addClass('col-sm-4 control-label')
	    			.text("Effectif des contrôlés")
			       )
			.append($('<div>')
				.addClass('col-sm-8')
	    			.append($('<input>')
	    				.addClass('form-control')
	    				.attr({
					    'id': 'Cinput',
					    'type': 'email',
					    'placeholder': 'Effectif de C',
					    'value': defIdfVal.C
					})
	    			       )
			       )
	    	       )
		.append($('<div>')
	    		.addClass('form-group')
	    		.append($('<label>')
				.attr('for', "Pinput")
				.addClass('col-sm-4 control-label')
	    			.text("Effectif des paniqués")
			       )
			.append($('<div>')
				.addClass('col-sm-8')
	    			.append($('<input>')
	    				.addClass('form-control')
	    				.attr({
					    'id': 'Pinput',
					    'type': 'email',
					    'placeholder': 'Effectif de P',
					    'value': defIdfVal.P
					})
	    			       )
			       )
	    	       )
		.append($('<div>')
	    		.addClass('form-group')
	    		.append($('<label>')
				.attr('for', "Binput")
				.addClass('col-sm-4 control-label')
	    			.text("Effectif des quotidiens 2")
			       )
			.append($('<div>')
				.addClass('col-sm-8')
	    			.append($('<input>')
	    				.addClass('form-control')
	    				.attr({
					    'id': 'Binput',
					    'type': 'email',
					    'placeholder': 'Effectif de B',
					    'value': defIdfVal.B
					})
	    			       )
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


function genEdgeModal(idw, idf) {
    cleanModal(idw);
    var modal = $(idw);
    // var defIdfVal = LinesGroup._layers[idf].options;


    modal.find('.modal-title').text('Lien ' + idf);


    //Gen table
    var table = $('<table>');

    $([[1,0,1], [1,1,1], [0,0,1]]).each(
    	function(){
    	    var line = $('<tr>');
    	    $(this).each(
    		function() {
    		    line.append($('<td>').html(this));
    		}
    	    );
    	    table.append(line);
    	}
    );

    modal.find('.modal-body')
	.append($('<div>')
		.append(table)
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
			    function(){
				updateEdgesData(idf, {
				    'cpMat': extractTable("#GenericModal table")
				});
				// Fermeture
				$("#GenericModal").modal("hide");
			    }
			   )
			.text("Valider")
		       )
	       );


    function drawTable() {


    }

    function extractTable(id) {
	var list = [];
	$(id).children()
	    .each(
		function(){
		    var row=[];
		    $(this).children()
			.each(
			    function(){
				var modality = parseFloat($(this).html());
				row.push(modality);
			    }
			);
		    list.push(row);
		}
	    );
	return list;
    }




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


function genSimModal (id) {
    cleanModal(id);
    var modal = $(id);
    // Set title
    modal.find('.modal-title').text('Simulation');

    var nbNoeuds = Object.keys(markersGroup._layers).length,
	nbLiens = Object.keys(linesGroup._layers).length;


    var TextGen = [nbNoeuds, nbLiens].map(
	function (x) {
	    var res;

	    switch(x) {
	    case 0:
		res = ["Aucun", ""];
		break;
	    case 1:
		res = [x, ""];
		break;
	    default:
		res = [x, "s"];
	    }
	    return res;
	}
    );

    var textN = `${TextGen[0][0]} noeud${TextGen[0][1]}`,
	textE = `${TextGen[1][0]} lien${TextGen[1][1]}`;

    modal.find('.modal-body')
	.append($('<div>')
		.append($('<ul>')
			.append($('<li>')
				.text(textN)
			       )
			.append($('<li>')
				.text(textE)
			       )
		       ));



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
			    function(){
				console.log("yep");
			    }
			   )
			.text("Valider")
		       )
	       );

}


function cleanModal (id) {
    var modal = $(id);
    modal.find('.modal-title').text('Void');
    modal.find('.modal-body').empty();
    modal.find('.modal-footer').empty();
}
