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
		.append($('<td>').text(sim.catastrophe_type).addClass("text-center"))
		.append($('<td>').text(sim.duration).addClass("text-center"))
		.append($('<td>').text(sim.timestep).addClass("text-center"))
		.append($('<td>').text(date).addClass("text-center"))
	       );

}

function resClean(idw) {}
