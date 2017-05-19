"use strict";

// Event on .feature-row
$(document)
// Zoom on map on tr click
// Ne zoome pas au click sur btn options
    .on('click', '.feature-row > td:not(.btn-marker-col)', function () {
	var id = $(this).parent().attr('id');
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

// Btn fermeture panneau
$("#sidebar-toggle-btn").click(
    function() {
	animateSidebar();
	return false;
    }
);

// Btn fermeture panneau
$("#sidebar-hide-btn").click(
    function() {
	animateSidebar();
	return false;
    }
);

// Btn suppresion markers
$("#sidebar-deleteMarkers-btn").click(
    function() {
	deleteAllMarkers();
	return false;
    }
);

// Ouverture/fermeture panneau
function animateSidebar() {
    $("#sidebar").animate({
	width: "toggle"
    }, 350, function() {
	map.invalidateSize();
    });
}

// Ouverture fenêtre importation
$("#sidebar-import-btn").click(
    function() {
	genImportModal("#GenericModal");
	$("#GenericModal").modal("show");
    }
);

$(document).on('click', 'button[id^=btn_mark_]',
	       function() {
		   var markerid = $(this).closest("tr").attr("id");
		   genFeatureModal("#GenericModal", markerid);
		   $("#GenericModal").modal("show");
    }
);

// Recentrer la vue
$("#sidebar-center-btn").click(
    function() {
	map.setView(defaultVue.coords, defaultVue.zoom);
    }
);

// Marker in sidebar on click
function markerClickSidebar (id) {
    var layer = map._layers[id];
    map.setView(
	[
	    layer.getLatLng().lat,
	    layer.getLatLng().lng
	], map.getZoom());
}

// Marker in sidebar on mouseover
function markerMouseoverSidebar (id) {
    var layer = map._layers[id];
    layer.setIcon(iconRed);
}

// Marker in sidebar on mouseout
function markerMouseoutSidebar (id) {
    var layer = map._layers[id];
    layer.setIcon(iconBlue);
}

// Add marker
function markerAddSidebar(id, a) {
    //console.log(id);
    $("#feature-list tbody")
	.append($('<tr>')
		.attr('id', id)
		.addClass("feature-row")
		.append($('<td>')
			.text(a[0])
			.addClass("text-center")
		       )
		.append($('<td>')
			.text(a[1])
			.addClass("text-center")
		       )
		.append($('<td>')
			.addClass("btn-marker-col")
			.append($('<div>')
				.append($('<button>')
					.attr(
					    {
						id: 'btn_mark_' + id,
						type:"button",
						class:"btn btn-xs btn-primary btn-outline"
					    }
					)
					.append($('<i>')
						.addClass("fa fa-wrench")
					       )
				       )
			       )
		       )
	       );
}

// Remove marker
function markerRemoveSidebar(id) {
    $(".feature-row[id*=" + id + "]").remove();
}

// Delete all markers
function deleteAllMarkers() {
    markersGroup.eachLayer(
	function (layer) {
	    var id = layer._leaflet_id;
	    markersGroup.removeLayer(layer);
	    markerRemoveSidebar(id);
	}
    );
}

function updateMarkerData(id, data) {
    var marker = markersGroup.getLayer(id).options;

    for(var prop in data) {
	marker[prop] = data[prop];
    }
}

function markerUpdateTableValues(id, a) {
    $("#feature-list tbody tr[id*=" + id + "] td")
	.each(
	    function(i, v) {
		$(this).text(a[i]);
	    }
	);
}
