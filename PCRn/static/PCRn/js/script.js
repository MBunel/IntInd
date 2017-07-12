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
    })
    .on('click', 'h3[class=panel-title] span', function() {
	changePanelSidebar();
    })
    .on('mouseover','h3[class=panel-title] span', function() {
	$(this).addClass('titleOver');
    })
    .on('mouseout','h3[class=panel-title] span', function() {
	$(this).removeClass('titleOver');
    });

// Btn fermeture panneau
$("#sidebar-hide-btn, #sidebar-toggle-btn").click(
    function() {
	var features = $('#left-sidebar > div > .features');
	if(features.is(':visible')) {
	    features.hide();
	    animateSidebar("#left-sidebar");
	} else {
	    animateSidebar("#left-sidebar");
	    features.show();
	}
	return false;
    }
);

// Btn fermeture panneau
$("#right-sidebar-hide-btn, #sidebar-right-toggle-btn").click(
    function() {
	var features = $('#right-sidebar > div > .features');
	if(features.is(':visible')) {
	    features.hide();
	    animateSidebar("#right-sidebar");
	} else {
	    animateSidebar("#right-sidebar");
	    features.show();
	}
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
function animateSidebar(id) {
    $(id).animate({
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
    $("#markers-list tbody")
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
    $("#markers-list tbody .feature-row[id*=" + id + "]").remove();
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
    $("#markers-list tbody tr[id*=" + id + "] td")
	.each(
	    function(i, v) {
		$(this).text(a[i]);
	    }
	);
}

function lineAddSidebar(id, a) {
    $("#lines-list tbody")
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
	       );
}

function lineRemoveSidebar(id) {
    $("#lines-list tbody .feature-row[id*=" + id + "]").remove();
}

// Alerter la visibilité des tables
function changePanelSidebar() {
    const Title = ["Marqueurs", "Liens", "Paramètres"];

    // On sélectionne la table suivant la (première) table visible
    var a = $('.sidebar-table table:visible:first').next();
    // Si il n'y à pas de table sélectionnée
    if (!a.length) {
	// On sélectionne la première
	a = $(".sidebar-table table:first");
    }
    // Puis on la rend visible
    a.css("display", "");
    // Et on masque le reste
    a.siblings().css("display", "none");

    var aInd = a.index();
    $('h3[class=panel-title] span').text(Title[aInd]);

}



/*
    Écriture des fonctions pour les requêtes POST
    Lancement de la simulation
 */


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});

function runSimulation() {
    $.ajax({
	type: "POST",
	url: 'runSim',
	dataType: "json",
	data: JSON.stringify({
	    'nodes': markersGroup.getLayers().map(function(x){
		var json = {};
		json['_l_id'] = x._leaflet_id;

		return json;
	    }),
	    'edges': linesGroup.getLayers().map(function(x){
		var json = {};
		json['_l_id'] = x._leaflet_id;
		json['idP'] = x.options.idPoints;

		return json;
	    })
	}),
	success: function(data){
	    console.log(data);
	    console.log("sucess callback");
	}
    });
}
