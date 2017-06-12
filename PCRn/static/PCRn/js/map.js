"use strict";

const appName = "PCRn/";

const defaultVue = {
    coords: [43.7, 7.25],
    zoom: 13
};

// Map creation
var map = L.map('mapid')
    .setView(defaultVue.coords, defaultVue.zoom)
    .on('click',
	function(e) {
	    pointPicker.SuppPoints();
	    onMapClick(e);
	}
       )
    .on('zoom',
	function() {
	    var markers = markersGroup.getLayers();

	    for (var markerid in markers) {
		var marker = markers[markerid];

		var latLng = marker.getLatLng(),
		    fixed = coordDecCalc(map.getZoom()),
		    lat = latLng.lat.toFixed(fixed),
		    lon = latLng.lng.toFixed(fixed),
		    id = marker._leaflet_id;
		markerUpdateTableValues(id, [lat, lon]);
	    }
	}
       );

var zoomDecParameters = {};

zoomDecParameters['zoomMin'] = map.options.minZoom || 11;
zoomDecParameters['zoomMax'] = map.options.maxZoom || 20;
zoomDecParameters['factorMin'] = 2;
zoomDecParameters['factorMax'] = 5;
zoomDecParameters['a'] = (
    (zoomDecParameters['factorMax'] - zoomDecParameters['factorMin']) /
	(zoomDecParameters['zoomMax'] - zoomDecParameters['zoomMin'])
);
zoomDecParameters['b'] = (
    zoomDecParameters['factorMin'] -
	zoomDecParameters['a']*zoomDecParameters['zoomMin']
);

// TileLayer definition
var TileLayer = L.tileLayer('https://{s}.tile.openstreetmap.fr/osmfr/{z}/{x}/{y}.{ext}', {
    attribution: 'Map',
    maxZoom: 20,
    ext: 'png'
}).addTo(map);

// Définition paramètres icône partagés
const icon = {
    iconSize: [20, 30],
    iconAnchor: [10, 30]
};

// Définition icône de base
const iconBlue = L.icon(
    // Fusion des objets
    Object.assign(
	{iconUrl: static_url +  appName + 'img/placeholder.svg'}, icon
    )
);

// Définition icône rouge
const iconRed = L.icon(
    Object.assign(
	{iconUrl: static_url + appName + 'img/placeholderred.svg'}, icon
    )
);

// Définiton Groupe de marqueurs
var markersGroup = new L.featureGroup()
    .on('layerremove',
	function(e) {
	    /*
	     * Identifiant du point supprimé
	     * identifiant des couches liés au point
	     */
	    var pointid = e.layer._leaflet_id,
		linkid = e.layer.options.idLines;
	    for (var i in linkid) {
		removeLine(i);
	    }
	}
       )
    .addTo(map);

// Définition Groupe de lignes
var linesGroup = new L.featureGroup()
    .addTo(map);


// Action au clic sur la carte
function onMapClick(e) {
    var newMarker = new L.marker(e.latlng, {
	// marker déplacable
	draggable: true,
	icon: iconBlue
    })
    // Ajout au tableau
	.on('add',
	    function (e) {
		var latLng = e.target.getLatLng(),
		    fixed = coordDecCalc(map.getZoom()),
		    lat = latLng.lat.toFixed(fixed),
		    lon = latLng.lng.toFixed(fixed),
		    id = e.target._leaflet_id;
		markerAddSidebar(id, [lat, lon]);
	    }
	   )
    // Suppression marker clic droit
	.on('contextmenu',
	    function () {
		var id = this._leaflet_id;
		markersGroup.removeLayer(this);
		markerRemoveSidebar(id);
	    }
	   )
    // Changement type au clic
	.on('click',
	    function (e) {
		pointPicker.AjoutPoint(this);
	    }
	   )
	.on('move',
	    function(e) {
		var latLng = e.target.getLatLng(),
		    fixed = coordDecCalc(map.getZoom()),
		    lat = latLng.lat.toFixed(fixed),
		    lon = latLng.lng.toFixed(fixed),
		    id = e.target._leaflet_id;

		markerUpdateTableValues(id, [lat, lon]);

		var linesLayers = linesGroup.getLayers();

		if (linesLayers.length !== 0) {
		    for (var layer in linesLayers) {
			movePointLine(layer);
		    }
		}
	    }
	   )
		.addTo(markersGroup);
}


function addLine(m1, m2) {

    var idM1 = m1._leaflet_id,
	idM2 = m2._leaflet_id,
	latLngM1 = m1.getLatLng(),
	latLngM2 = m2.getLatLng(),
	latM1 = latLngM1.lat,
	lngM1 = latLngM1.lng,
	latM2 = latLngM2.lat,
	lngM2 = latLngM2.lng,
	coords = [[latM1, lngM1], [latM2, lngM2]];

    var newLine = new L.polyline(coords)
	.on('contextmenu',
	    function() {
		var id = this._leaflet_id;
		removeLine(id);
	    }
	   );

    newLine.addTo(linesGroup);

    newLine['options']['idPoints'] = {};
    newLine['options']['idPoints'][0] = idM1;
    newLine['options']['idPoints'][1] = idM2;

    if (m1['options']['idLines'] === undefined) {
	m1['options']['idLines'] = {};
    }
    if (m2['options']['idLines'] === undefined) {
	m2['options']['idLines'] = {};
    }

    m1['options']['idLines'][newLine._leaflet_id] = 0;
    m2['options']['idLines'][newLine._leaflet_id] = 1;

    return newLine._leaflet_id;

}

function movePointLine(id) {
    // Récupération de la polyligne
    var layer = linesGroup.getLayers()[id];
    var newCoords = [];
    $.each(layer['options']['idPoints'],
	   function (i,v) {
	       var latlng = markersGroup.getLayer(v).getLatLng();
	       newCoords.push(new L.LatLng(latlng.lat, latlng.lng));
	   }
	  );
    layer.setLatLngs(newCoords);
}

function linePointsClear(id) {
    /*
     * Identifiant de la couche ligne
     * Identifiant des points liés à la couche ligne
     */
    var layer = linesGroup.getLayer(id),
	linepoint = layer.options.idPoints;

    $.each(linepoint,
	   function(index, v) {
	       // Couche de points liés
	       var pointLayer = markersGroup.getLayer(v);
	       if (pointLayer !== undefined) {
		   // Supression info lien
		   delete pointLayer.options.idLines[id];
	       }
	   }
	  );
}

function removeLine(id) {
    linePointsClear(id);
    linesGroup.removeLayer(id);
    lineRemoveSidebar(id);
}

// Lister marqueurs
function markerList() {
    var allMarkersObjArray = [];
    var allMarkersGeoJsonArray = [];

    $.each(map._layers, function (ml) {
        //console.log(map._layers)
        if (map._layers[ml]._layers) {

	    $.each(this._layers, function () {
		allMarkersObjArray.push(this);
		allMarkersGeoJsonArray.push(JSON.stringify(this.toGeoJSON()));
	    });
	}
    });
    console.log(allMarkersGeoJsonArray);
}

function coordDecCalc(zoom) {
    var params = zoomDecParameters,
	a = params['a'],
	b = params['b'];

    var factor = a*zoom + b;

    return factor < 1 ? 1  : Math.round(factor);

}


var PointPicker = function () {
    this.points = [];

};

PointPicker.prototype.AjoutPoint = function(point) {
    if (this.points.length === 0 || this.points[0] !== point) {
	this.points.push(point);
	if (this.points.length === 2) {
	    this.ConstruireLigne();
	    this.SuppPoints();
	}
    }
};

PointPicker.prototype.ConstruireLigne = function() {
    var lineId = addLine(this.points[0], this.points[this.points.length - 1]);
    lineAddSidebar(lineId,
		   [
		       this.points[0]._leaflet_id,
		       this.points[1]._leaflet_id
		   ]);
};

PointPicker.prototype.SuppPoints = function() {
    this.points = [];
};

var pointPicker = new PointPicker();
