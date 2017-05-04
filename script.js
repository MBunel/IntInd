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


var markersGroup = new L.featureGroup()
    .addTo(map);

function onMapClick(e) {
    "use strict";
    var newMarlef = new L.marker(e.latlng, {
	// marker déplacable
	draggable: true
    })
    // Ajout au tableau
	.on('add',
	    function (e) {
		var latLng = e.target.getLatLng(),
		    lat = latLng.lat.toFixed(2),
		    lon = latLng.lng.toFixed(2);
		markerAddSidebar([lat, lon]);
	    }
	   )
    // Suppression marker clic droit
	.on('contextmenu',
	    function () {
		markersGroup.removeLayer(this);
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


function onMarkerLeftClick(e) {
    /* var newPopup = new L.popup()
       .setLatLng(e.latlng)
       .setContent("Popup")
       .openOn(map);
    */
}


// Add marker
function markerAddSidebar(a) {
    $("#feature-list tbody")
	.append($('<tr>')
		.addClass("feature-row")
		.append($('<td>').text(a[0]))
		.append($('<td>').text(a[1]))
	       );
}

$("#sidebar-toggle-btn").click(function() {
    animateSidebar();
    return false;
});

$("#sidebar-hide-btn").click(function() {
    animateSidebar();
    return false;
});

function animateSidebar() {
    $("#sidebar").animate({
	width: "toggle"
    }, 350, function() {
	map.invalidateSize();
    });
}
