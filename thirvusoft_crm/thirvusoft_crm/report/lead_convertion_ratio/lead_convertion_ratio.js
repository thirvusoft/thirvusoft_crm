// Copyright (c) 2024, Thirvusoft Private Limited and contributors
// For license information, please see license.txt

frappe.query_reports["Lead Convertion Ratio"] = {
	"filters": [
		{
			fieldname: 'from_date',
			label: 'From Date',
			fieldtype: 'Date',
			default: frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			reqd: 1
		},

		{
			fieldname: 'to_date',
			label: 'To Date',
			fieldtype: 'Date',
			default: 'Today',
			reqd: 1
		},

		{
			fieldname: 'type',
			label: 'Type',
			fieldtype: 'Select',
			options: 'Lead\nQuotation',
			reqd: 1,
			default: "Lead"
		},
	]
};
