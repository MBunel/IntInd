"use strict";

const defaultVue = {
    coords: [43.7, 7.25],
    zoom: 11
};

// Map creation
var map = L.map('mapid')
    .setView(defaultVue.coords, defaultVue.zoom)
    .on('click', onMapClick)
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
var TileLayer = L.tileLayer('http://stamen-tiles-{s}.a.ssl.fastly.net/toner-lite/{z}/{x}/{y}.{ext}', {
    attribution: 'Map',
    subdomains: 'abcd',
    minZoom: 0,
    maxZoom: 20,
    ext: 'png'
}).addTo(map);

// Définition paramètres icône partagés
const icon = {
    iconSize: [38, 95],
    iconAnchor: [15, 60]
};

// Définition icône de base
const iconBlue = L.icon(
    // Fusion des objets
    Object.assign(
	{iconUrl: 'img/placeholder.svg'}, icon
    )
);

// Définition icône rouge
const iconRed = L.icon(
    Object.assign(
	{iconUrl: 'img/placeholderred.svg'}, icon
    )
);

// Définiton Groupe de marqueurs
var markersGroup = new L.featureGroup()
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
		//console.log(e);
		// TODO
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
    //console.log(newMarker);
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

    var newLine = new L.polyline(coords);

    newLine['options']['idPoints'] = {};

    newLine['options']['idPoints'][0] = idM1;
    newLine['options']['idPoints'][1] = idM2;

    newLine.addTo(linesGroup);
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
