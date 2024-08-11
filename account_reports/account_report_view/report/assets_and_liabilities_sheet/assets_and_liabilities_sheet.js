// Copyright (c) 2024, Hadeel Milad and contributors
// For license information, please see license.txt

// frappe.query_reports["Assets and Liabilities Sheet"] = {
// 	"filters": [

// 	]
// };

// frappe.query_reports["Assets and Liabilities Sheet"] = {
// 	"filters": [

// 	]
// };
frappe.query_reports["Assets and Liabilities Sheet"] = $.extend({}, erpnext.financial_statements);
	frappe.query_reports["Assets and Liabilities Sheet"]["filters"].push({
		"fieldname": "accumulated_values",
		"label": __("Accumulated Values"),
		"fieldtype": "Check",
		"default": 1
	});
	
	frappe.query_reports["Assets and Liabilities Sheet"]["filters"].push({
		"fieldname": "include_default_book_entries",
		"label": __("Include Default Book Entries"),
		"fieldtype": "Check",
		"default": 1
	});
	
	frappe.query_reports["Assets and Liabilities Sheet"]["filters"][4].options = [{value: 'Yearly', label: 'Yearly'}];

// frappe.require("assets/erpnext/js/financial_statements.js", function() {
// 	frappe.query_reports["Assets and Liabilities Sheet"] = $.extend({}, erpnext.financial_statements);

// 	erpnext.utils.add_dimensions('Assets and Liabilities Sheet', 10);
	
// 	frappe.query_reports["Assets and Liabilities Sheet"]["filters"].push({
// 		"fieldname": "accumulated_values",
// 		"label": __("Accumulated Values"),
// 		"fieldtype": "Check",
// 		"default": 1
// 	});
	
// 	frappe.query_reports["Assets and Liabilities Sheet"]["filters"].push({
// 		"fieldname": "include_default_book_entries",
// 		"label": __("Include Default Book Entries"),
// 		"fieldtype": "Check",
// 		"default": 1
// 	});
	
// 	frappe.query_reports["Assets and Liabilities Sheet"]["filters"][4].options = [{value: 'Yearly', label: 'Yearly'}];
// });