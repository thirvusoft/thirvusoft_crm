// Copyright (c) 2024, Thirvusoft Private Limited and contributors
// For license information, please see license.txt

frappe.query_reports["Missed Follow Ups"] = {
	"filters": [
		{
			fieldname: 'date',
			label: 'Date',
			fieldtype: 'Date',
			default: frappe.datetime.get_today(),
			reqd: 1
		},
		{
			fieldname: 'user',
			label: 'Follow Up By',
			fieldtype: 'Autocomplete',
			options: []
		},
		{
			fieldname: 'lead',
			label: 'Lead',
			fieldtype: 'Check',
			default: 1
		},
		{
			fieldname: 'quotation',
			label: 'Quotation',
			fieldtype: 'Check',
			default: 1
		}
	],

	onload: function(report){
		frappe.db.get_value("User", {"name": frappe.session.user}, "username", (r) => {
			frappe.query_report.set_filter_value('user', r.username);
		})
	}
};
