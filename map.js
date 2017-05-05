"use strict";

var map = L.map('mapid')
    .setView([51.505, -0.09], 13)
    .on('click', onMapClick);

L.tileLayer('http://stamen-tiles-{s}.a.ssl.fastly.net/watercolor/{z}/{x}/{y}.{ext}', {
    attribution: 'Map tiles',
    subdomains: 'abcd',
    minZoom: 1,
    maxZoom: 16,
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

var markersGroup = new L.featureGroup()
    .addTo(map);

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
		    lat = latLng.lat.toFixed(2),
		    lon = latLng.lng.toFixed(2),
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
		console.log(e);
		// TODO
	    }
	   )
	.addTo(markersGroup);
    console.log(newMarker);
}

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
