$(function() {

    const a = [
	{
	    'orig': "div.table-responsive:nth-child(1) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(1)",
	    'dest': ["#rect-qt"]
	},
	{
	    'orig': "div.table-responsive:nth-child(1) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(2)",
	    'dest': ["#rect-bt"]
	},
	{
	    'orig': "div.table-responsive:nth-child(1) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(3)",
	    'dest': ["#rect-rt"]
	},
	{
	    'orig': "div.table-responsive:nth-child(1) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(4)",
	    'dest': ["#rect-ct"]
	},
	{
	    'orig': "div.table-responsive:nth-child(1) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(5)",
	    'dest': ["#rect-pt"]
	},
	{
	    'orig': "div.table-responsive:nth-child(1) > table:nth-child(1) > caption:nth-child(3)",
	    'dest': ["#rect-qt", "#rect-bt", "#rect-rt", "#rect-ct", "#rect-pt"]
	},
	{
	    'orig': "div.table-responsive:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1)",
	    'dest': ["#path-b1"]
	},
	{
	    'orig': "div.table-responsive:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(2)",
	    'dest': ["#path-b2"]
	},
	{
	    'orig': "div.table-responsive:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(3)",
	    'dest': ["#path-c1"]
	},
	{
	    'orig': "div.table-responsive:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(4)",
	    'dest': ["#path-c2"]
	},
	{
	    'orig': "div.table-responsive:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(5)",
	    'dest': ["#path-s1"]
	},
	{
	    'orig': "div.table-responsive:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(6)",
	    'dest': ["#path-s2"]
	},
	{
	    'orig': "div.table-responsive:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(7)",
	    'dest': ["#path-gammat"]
	},
	{
	    'orig': "div.table-responsive:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(8)",
	    'dest': ["#path-phit"]
	},
	{
	    'orig': "div.table-responsive:nth-child(2) > table:nth-child(1) > caption:nth-child(2)",
	    'dest': ["#path-b1", "#path-b2", "#path-c1", "#path-c2", "#path-s1", "#path-s2"]
	},
	{
	    'orig': "div.table-responsive:nth-child(3) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1)",
	    'dest': ["#g-alpha > *"]
	},
	{
	    'orig': "div.table-responsive:nth-child(3) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(2)",
	    'dest': ["#g-gamma > *"]
	},
	{
	    'orig': "div.table-responsive:nth-child(3) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(3)",
	    'dest': ["#g-mu > *"]
	},
	{
	    'orig': "div.table-responsive:nth-child(3) > table:nth-child(1) > caption:nth-child(2)",
	    'dest': ["#g-alpha > *", "#g-gamma > *", "#g-mu > *"]
	},

	{
	    'orig': "#rect-qt",
	    'dest': ["div.table-responsive:nth-child(1) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(1)"]
	},
	{
	    'orig': "#rect-bt",
	    'dest': ["div.table-responsive:nth-child(1) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(2)"]
	},
	{
	    'orig': "#rect-rt",
	    'dest': ["div.table-responsive:nth-child(1) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(3)"]
	},
	{
	    'orig': "#rect-ct",
	    'dest': ["div.table-responsive:nth-child(1) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(4)"]
	},
	{
	    'orig': "#rect-pt",
	    'dest': ["div.table-responsive:nth-child(1) > table:nth-child(1) > tbody:nth-child(2) > tr:nth-child(5)"]
	},

	{
	    'orig': "#path-b1",
	    'dest': ["div.table-responsive:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1)"]
	},
	{
	    'orig': "#path-b2",
	    'dest': ["div.table-responsive:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(2)"]
	},
	{
	    'orig': "#path-c1",
	    'dest': ["div.table-responsive:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(3)"]
	},
	{
	    'orig': "#path-c2",
	    'dest': ["div.table-responsive:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(4)"]
	},
	{
	    'orig': "#path-s1",
	    'dest': ["div.table-responsive:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(5)"]
	},
	{
	    'orig': "#path-s2",
	    'dest': ["div.table-responsive:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(6)"]
	},
	{
	    'orig': "#path-gammat",
	    'dest': ["div.table-responsive:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(7)"]
	},
	{
	    'orig': "#path-phit",
	    'dest': ["div.table-responsive:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(8)"]
	},

	{
	    'orig': "#g-alpha > *",
	    'dest': ["div.table-responsive:nth-child(3) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1)"]
	},
	{
	    'orig': "#g-gamma > *",
	    'dest': ["div.table-responsive:nth-child(3) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(2)"]
	},
	{
	    'orig': "#g-mu > *",
	    'dest': ["div.table-responsive:nth-child(3) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(3)"]
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
