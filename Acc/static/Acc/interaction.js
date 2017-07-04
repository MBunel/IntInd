$(function() {

    const a = [
	{
	    'orig': "div.table-responsive:nth-child(1) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(1)",
	    'dest': ["#gr-qt"]
	},
	{
	    'orig': "div.table-responsive:nth-child(1) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(2)",
	    'dest': ["#gr-bt"]
	},
	{
	    'orig': "div.table-responsive:nth-child(1) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(3)",
	    'dest': ["#gr-rt"]
	},
	{
	    'orig': "div.table-responsive:nth-child(1) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(4)",
	    'dest': ["#gr-ct"]
	},
	{
	    'orig': "div.table-responsive:nth-child(1) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(5)",
	    'dest': ["#gr-pt"]
	},
	{
	    'orig': "div.table-responsive:nth-child(1) > table:nth-child(1) > caption:nth-child(3)",
	    'dest': ["#gr-qt", "#gr-bt", "#gr-rt", "#gr-ct", "#gr-pt"]
	},
	{
	    'orig': "div.table-responsive:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1)",
	    'dest': ["#gr-b1"]
	},
	{
	    'orig': "div.table-responsive:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(2)",
	    'dest': ["#gr-b2"]
	},
	{
	    'orig': "div.table-responsive:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(3)",
	    'dest': ["#gr-c1"]
	},
	{
	    'orig': "div.table-responsive:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(4)",
	    'dest': ["#gr-c2"]
	},
	{
	    'orig': "div.table-responsive:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(5)",
	    'dest': ["#gr-s1"]
	},
	{
	    'orig': "div.table-responsive:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(6)",
	    'dest': ["#gr-s2"]
	},
	{
	    'orig': "div.table-responsive:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(7)",
	    'dest': ["#Forcage", "#g7458", "#g7351", "#use5166"]
	},
	{
	    'orig': "div.table-responsive:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(8)",
	    'dest': ["#gr-phi"]
	},
	{
	    'orig': "div.table-responsive:nth-child(2) > table:nth-child(1) > caption:nth-child(2)",
	    'dest': ["#gr-b1", "#gr-b2", "#gr-c1", "#gr-c2", "#gr-s1", "#gr-s2", "#Forcage", "#gr-phi"]
	},
	{
	    'orig': "div.table-responsive:nth-child(3) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1)",
	    'dest': ["#gr-a1", "#gr-a2"]
	},
	{
	    'orig': "div.table-responsive:nth-child(3) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(2)",
	    'dest': ["#gr-d1", "#gr-d2"]
	},
	{
	    'orig': "div.table-responsive:nth-child(3) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(3)",
	    'dest': ["#gr-mu1", "#gr-mu2"]
	},
	{
	    'orig': "div.table-responsive:nth-child(3) > table:nth-child(1) > caption:nth-child(2)",
	    'dest': ["#gr-a1", "#gr-d1", "#gr-mu1", "#gr-a2", "#gr-d2", "#gr-mu2"]
	},




	{
	    'orig': "#gr-qt",
	    'dest': ["div.table-responsive:nth-child(1) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(1)"]
	},
	{
	    'orig': "#gr-bt",
	    'dest': ["div.table-responsive:nth-child(1) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(2)"]
	},
	{
	    'orig': "#gr-rt",
	    'dest': ["div.table-responsive:nth-child(1) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(3)"]
	},
	{
	    'orig': "#gr-ct",
	    'dest': ["div.table-responsive:nth-child(1) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(4)"]
	},
	{
	    'orig': "#gr-pt",
	    'dest': ["div.table-responsive:nth-child(1) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(5)"]
	},

	{
	    'orig': "#gr-b1",
	    'dest': ["div.table-responsive:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1)"]
	},
	{
	    'orig': "#gr-b2",
	    'dest': ["div.table-responsive:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(2)"]
	},
	{
	    'orig': "#gr-c1",
	    'dest': ["div.table-responsive:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(3)"]
	},
	{
	    'orig': "#gr-c2",
	    'dest': ["div.table-responsive:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(4)"]
	},
	{
	    'orig': "#gr-s1",
	    'dest': ["div.table-responsive:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(5)"]
	},
	{
	    'orig': "#gr-s2",
	    'dest': ["div.table-responsive:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(6)"]
	},
	{
	    'orig': "#Forcage",
	    'dest': ["div.table-responsive:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(7)"]
	},
	{
	    'orig': "#gr-phi",
	    'dest': ["div.table-responsive:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(8)"]
	},

	{
	    'orig': "#gr-a1, #gr-a2",
	    'dest': ["div.table-responsive:nth-child(3) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1)"]
	},
	{
	    'orig': "#gr-d1, #gr-d2",
	    'dest': ["div.table-responsive:nth-child(3) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(2)"]
	},
	{
	    'orig': "#gr-mu1, #gr-mu2",
	    'dest': ["div.table-responsive:nth-child(3) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(3)"]
	},







	{
	    'orig': '#ell1',
	    'dest': [
		"div.table-responsive:nth-child(1) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(4)"
	    ]
	},
	{
	    'orig': '#ell2',
	    'dest': [
		"div.table-responsive:nth-child(1) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(3)",
		"div.table-responsive:nth-child(1) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(5)",
		"div.table-responsive:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(2)",
		"div.table-responsive:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(6)",
		"div.table-responsive:nth-child(3) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(2)"
	    ]
	}
    ];

    a.map(function(x) {
	$(x['orig'])
	    .on("mouseover", function() {
		var dest = x['dest'].toString();
		$(dest).addClass("hover");
	    })
	    .on("mouseout", function() {
		var dest = x['dest'].toString();
		$(dest).removeClass("hover");
	    });
    });

});
