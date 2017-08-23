"use strict";


function resAppendSimulation(sim) {
    // Transformation des dates

    var date;
    var inputDate = new Date(sim.timestamp);
    var todaysDate = new Date();

    if(inputDate.toDateString() !== todaysDate.toDateString()) {
	date = inputDate.toLocaleDateString('fr-FR',
					    {hour: '2-digit', minute:'2-digit'});
    } else {
	date = inputDate.getHours() + ":" + inputDate.getMinutes();
    }


    $("#simulation-list")
		.append($('<tr>')
			.attr('id', sim.id)
			.addClass("feature-row")
			.append($('<td>')
				.append($('<button>')
					.attr("type", 'button')
					.addClass("btn btn-xs btn-default sidebar-button")
					.click(
					    function(){
						$(this)
						    .find('i')
						    .toggleClass("fa-plus-square fa-minus-square");
						showSimulationDetails(sim.id);
					    })
					.append($('<i>')
						.addClass("fa fa-plus-square"))))
			.append($('<td>')
				.text(sim.catastrophe_type)
				.addClass("text-center"))
			.append($('<td>')
				.text(sim.duration)
				.addClass("text-center"))
			.append($('<td>')
				.text(sim.timestep)
				.addClass("text-center"))
			.append($('<td>')
				.text(date)
				.addClass("text-center"))
	       );

}


function showSimulationDetails(simId) {
    console.log(simId);
    var row = $("#simulation-list");
    var rowDetails = row.find('#' + simId +'[type=details]');

    if (rowDetails.length === 0) {
	resAppendSimulationDetails(simId, row);
    } else {
	rowDetails.toggle();
    }

}

function resAppendSimulationDetails(simId, row) {
	// Création tableau
	row.append($('<tr>')
		   .attr('id', simId)
		   .attr('type', 'details')
		   .addClass("feature-row")
		   .append($('<table>')
			   //.addClass("sidebar-table")
			   .append($('<tbody>')
				   .addClass("table table-hover table-striped table-condensed")
				   .append($('<tr>')
					   .addClass("feature-row")
					  )
				  )
			  )
		  );

    //var results = getSimulationParameters(simId);
}


function resClean(idw) {}


function getSimulationsList() {
    $.ajax({
	type: "GET",
	url: "getSims",
	dataType: "json",
	success: function(data) {
	    console.log(data);
	},
	error: function() {
	    console.log('error');
	}
    });
}

function getSimulationParameters(simid) {
    $.ajax({
	type: "GET",
	url: "getSimParams",
	dataType: "json",
	data: {'simid': simid},
	success: function(data) {
	    return data;
	},
	error: function() {
	    console.log('error');
	}
    });
}

function getSimulationData(simid) {
    $.ajax({
	type: "GET",
	url: "getSimData",
	dataType: "json",
	data: {'simid': simid},
	success: function(data) {
	    console.log(data);
	},
	error: function() {
	    console.log('error');
	}
    });
}
