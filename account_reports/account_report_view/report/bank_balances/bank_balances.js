// Copyright (c) 2024, Hadeel Milad and contributors
// For license information, please see license.txt

frappe.query_reports["Bank Balances"] = {
	"filters": [
		{
			"fieldname": "company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company"),
		},
		{
			"fieldname": "account",
			"label": __("Account"),
			"fieldtype": "Link",
			"options": "Account",
			"get_query": function() {
				return {
					"filters": {
						"account_type": "Bank",
					}
				}
			}
		}
	]
};