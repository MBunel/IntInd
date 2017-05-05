"use strict";

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

$("#sidebar-toggle-btn").click(
    function() {
	animateSidebar();
	return false;
    }
);

$("#sidebar-hide-btn").click(
    function() {
	animateSidebar();
	return false;
    }
);

$("#sidebar-deleteMarkers-btn").click(
    function() {
	deleteAllMarkers();
	return false;
    }
);

function animateSidebar() {
    $("#sidebar").animate({
	width: "toggle"
    }, 350, function() {
	map.invalidateSize();
    });
}

$("#sidebar-import-btn").click(
    function() {
	$("#featureModal").modal("show");
    }
);

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

function deleteAllMarkers() {
    markersGroup.eachLayer(
	function (layer) {
	    var id = layer._leaflet_id;
	    markersGroup.removeLayer(layer);
	    markerRemoveSidebar(id);
	}
    );
}
