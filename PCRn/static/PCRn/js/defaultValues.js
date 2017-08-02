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
		.addClass("feature-row")
		.append($('<td>')
			.text(i.capitalize())
			.addClass("text-center")
		       )
		.append($('<td>')
			.text(v)
			.addClass("text-center")
		       )
	);
    });
};



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
    'step': 0.1
});

defaultModelValues.genTable('global');
