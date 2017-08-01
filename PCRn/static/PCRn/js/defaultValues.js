var DefaultParameters = function () {
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


var defaultModelValues = new DefaultParameters();
