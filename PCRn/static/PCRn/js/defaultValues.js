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
    out.append($('<tr>')
	       .append($('<td>')
		       .html(type)
		      )
	      );
    $.each(obj, function(i,v){
	out.append(
	    $('<tr>')
		.append($('<td>')
			.html(i)
		       )
		.append($('<td>')
			.html(v)
		       )
	);
    });
};



var defaultModelValues = new DefaultParameters('#parameters-list > tbody');

// ex
// defaultModelValues.updateParameter('nodes', {'merguez':2, 'bière':2});
// defaultModelValues.genTable('nodes')
