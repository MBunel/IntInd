var DefaultParameters = function (tableid) {
    this.tableid = tableid;

    this.defaultNodes = {};
    this.defaultEdges = {};
    this.defaultGlobal = {};
};

DefaultParameters.prototype.parseType = function(type) {
    var params;
    switch(type) {
    case 'nodes':
	params = this.defaultNodes;
	break;
    case 'edges':
	params = this.defaultEdges;
	break;
    case 'global':
	params = this.defaultGlobal;
	break;
    }
    return params;
};

DefaultParameters.prototype.updateParameter = function(type, parameters) {
    var obj = this.parseType(type);
    for(var param in parameters) {
	obj[param] = parameters[param];
    }
};

DefaultParameters.prototype.getParameter = function(type) {
    return this.parseType(type);
};

DefaultParameters.prototype.genTable = function(type) {
    var obj = this.parseType(type);
    var out = $(this.tableid);
    $.each(obj, function(i,v){
	out.append(
	    $('<tr>')
		.addClass("feature-row globalOption-row")
		.append($('<td>')
			.text(i.capitalize())
			.addClass("text-left")
		       )
		.append($('<td>')
			.addClass("text-center globalOption-value")
			.attr("paramkey", i)
			.text(v)
		       )
	);
    });
};

$(document)
    .on('click', '.globalOption-value', function () {
	var def = $(this);
	def.removeClass("globalOption-value");
	var selector = $('<form>')
	    .addClass("selectorDiv form-inline")
	    .append($('<input>')
		    .addClass('input-sm form-control')
		    .val(def.text())
		   )
	    .append(
		$('<button>')
		    .addClass("btn btn-xs btn-primary btn-outline parameter-changer")
		    .attr("type", "button")
		    .append($('<i>').addClass("fa fa-check"))
	    );
	def.html("").append(selector);
    })
	.on('click', '.parameter-changer', function(){
	    var $this = $(this);
	    var $gop = $this.closest(".selectorDiv");
	    var $gopp = $gop.parent();
	    var key = $gopp.attr("paramkey");
	    var val = $gop.children("input").val();
	    $gopp.addClass("globalOption-value");
	    $gopp.empty();
	    $gopp.text(val);
	    // On met à jour la valeur dans l'objet
	    // le [] sert à ce que ce soit la valeur de key qui soit la
	    // clé et non la chaine "key"
	    defaultModelValues.updateParameter('global', {[key]: val});
	});


var defaultModelValues = new DefaultParameters('#parameters-list > tbody');

// Les variables par défaut sont fixées dans le code
// Système à modifier

// params def nodes
defaultModelValues.updateParameter('nodes', {
    'Q':2,
    'R':2,
    'C':2,
    'P':2,
    'B':2
});

// params def edges
defaultModelValues.updateParameter('edges', {
    'cpMat': [[0, 0, 1], [0, 1, 1], [1,1,1,]]
});

// global param
defaultModelValues.updateParameter('global', {
    'time': 60,
    'step': 0.1,
    'saucisse' : 22,
    'bière': 'oui',
    'Effectif de A': 30
});

defaultModelValues.genTable('global');
