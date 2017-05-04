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

const icon = {
    iconSize: [38, 95],
    iconAnchor: [15, 60]
};

const iconBlue = L.icon(
    Object.assign(
	{iconUrl: 'placeholder.svg'}, icon
    )
);

const iconRed = L.icon(
    Object.assign(
	{iconUrl: 'placeholderred.svg'}, icon
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

// Add marker
function markerAddSidebar(id, a) {
    console.log(id);
    $("#feature-list tbody")
	.append($('<tr>')
		.attr('id', id)
		.addClass("feature-row")
		.append($('<td>').text(a[0]))
		.append($('<td>').text(a[1]))
	       );
}

// Remove marker
function markerRemoveSidebar(id) {
    $(".feature-row[id*=" + id + "]").remove();
}

// Event on .feature-row
$(document)
// Zoom on map on tr click
    .on('click', '.feature-row', function () {
	var id = $(this).attr('id');
	markerClickSidebar(id);
    })
    .on('mouseover', '.feature-row', function() {
	var id = $(this).attr('id');
	markerMouseoverSidebar(id);
    })
    .on('mouseout', '.feature-row', function() {
	var id = $(this).attr('id');
	markerMouseoutSidebar(id);
    });

// Sidebar on click
function markerClickSidebar (id) {
    var layer = map._layers[id];
    map.setView([layer.getLatLng().lat, layer.getLatLng().lng], 17);
}

// Sidebar on mouseover
function markerMouseoverSidebar (id) {
    var layer = map._layers[id];
    layer.setIcon(iconRed);
}

// Sidebar on mouseout
function markerMouseoutSidebar (id) {
    var layer = map._layers[id];
    layer.setIcon(iconBlue);
}

function deleteAllMarkers() {
    markersGroup.eachLayer(
	function (layer) {
	    var id = layer._leaflet_id;
	    markersGroup.removeLayer(layer);
	    markerRemoveSidebar(id);
	}
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
