# Copyright (c) 2024, Thirvusoft Private Limited and contributors
# For license information, please see license.txt

import frappe

def execute(filters = None):

	columns = get_columns(filters)

	data = get_data(filters)

	return columns, data

def get_columns(filters):

	columns = [

		{
			'fieldname': 'name',
			'fieldtype': 'Data',
			'label': 'Lead / Quotation ID',
			'width': 195
		},

		{
			'fieldname': 'lead_name',
			'fieldtype': 'Data',
			'label': 'Lead / Quotation Name',
			'width': 195
		},
		{
			'fieldname': 'company_name',
			'fieldtype': 'Data',
			'label': 'Organization',
			'width': 195
		},

		{
			'fieldname': 'lead_owner',
			'fieldtype': 'Data',
			'label': 'Lead / Quotation Owner',
			'width': 195
		},

		# {
		# 	'fieldname': 'territory',
		# 	'fieldtype': 'Link',
		# 	'label': 'Territory',
		# 	'options': 'Territory',
		# 	'width': 182
		# },

		{
			'fieldname': 'status',
			'fieldtype': 'Data',
			'label': 'Status',
			'width': 182
		},

		{
			'fieldname': 'contact_number',
			'fieldtype': 'Data',
			'label': 'Contact Number',
			'width': 182
		},
		{
			'fieldname': 'mode_of_communication',
			'fieldtype': 'Data',
			'label': 'Mode of Communication',
			'width': 195
		},

		{
			'fieldname': 'remarks',
			'fieldtype': 'Data',
			'label': 'Remarks',
			'width': 400
		},

		{
			'fieldname':'description',
			'fieldtype':'Small Text',
			'label':'Description',
			'width':400
		},
	]

	return columns

def get_data(filters):

	if filters.get('user'):

		filter_user = filters.get('user')

		filters["user"] = frappe.get_value("User", {"username": filter_user}, "name")

	data=[]
	if (filters.get('lead')):
		follow_up_filter = {}
		lead_filter = {'status':['not in', ['Do Not Contact', 'Quotation Created']]}
		if(filters.get('date')):
			follow_up_filter['next_follow_up_date'] = filters.get('date')
		if (filters.get('user')):
			follow_up_filter['next_follow_up_by'] = filters.get('user')

		all_leads = frappe.db.get_all('Follow-Up', filters=follow_up_filter, fields=['idx', 'parent','next_follow_up_by','description', 'mode_of_communication'])
		all_leads1=[]
		for i in all_leads:
			follow_up_filter['parent'] = i['parent']			
			if(max(frappe.db.get_all('Follow-Up', filters={'parent':i['parent']}, pluck='idx')) == i['idx']):
				if(not i.get("next_follow_up_by")):
					all_leads1.append(i)
				elif(not filters.get("user")):
					all_leads1.append(i)
				elif(filters.get("user") and i.get("next_follow_up_by")==filters.get("user")):
					all_leads1.append(i)
		desc={i['parent']:[i['description'],i.get("next_follow_up_by") or "", i.get("mode_of_communication") or ""] for i in all_leads1}


		leads = [i['parent'] for i in all_leads1]
		site_lead=leads
		lead_filter['name'] = ['in', site_lead]
		leads = frappe.db.get_all('Lead', filters=lead_filter, fields=['name', 'lead_name', 'lead_owner','status', 'custom_remarks as remarks', 'company_name'])

		for i in leads:
			i['description']=desc[i["name"]][0]
			i['next_followup_by']=desc[i["name"]][1]
			i['mode_of_communication']=desc[i["name"]][2]

			contact=frappe.get_all(
				"Contact",
					filters=[
					["Dynamic Link", "link_doctype", "=", 'Lead'],
					["Dynamic Link", "link_name", "=", i['name']],
					["Contact Phone", 'is_primary_mobile_no', "=", 1]
					],
					fields=['`tabContact Phone`.phone'],
					order_by='`tabContact`.creation desc'
				)
			if contact:
				i['contact_number']=contact[0]['phone']
    
			i['name'] = f'''<button style=" font-size: 13px;  background-color: #000000;color: #ffffff;border-radius: 5px; height: 24px;" onclick='frappe.set_route("Form", "Lead", "{i["name"]}" )'>
			{i["name"]}
			</button>'''
   
		data+=leads
		
	if (filters.get('quotation')):
		follow_up_filter = {}
		lead_filter={}
		lead_filter = {'docstatus':['not in', [2]]}

		if(filters.get('date')):
			follow_up_filter['next_follow_up_date'] = filters.get('date')
		if (filters.get('user')):
			follow_up_filter['next_follow_up_by'] = filters.get('user')

		all_leads = frappe.db.get_all('Follow-Up', filters=follow_up_filter, fields=['idx', 'parent','next_follow_up_by','description','mode_of_communication'])
		all_leads1=[]
		for i in all_leads:
			follow_up_filter['parent'] = i['parent']
			
			if(max(frappe.db.get_all('Follow-Up', filters={'parent':i['parent']}, pluck='idx')) == i['idx']):
				if(not i.get("next_follow_up_by")):
					all_leads1.append(i)
				elif(not filters.get("user")):
					all_leads1.append(i)
				elif(filters.get("user") and i.get("next_follow_up_by")==filters.get("user")):
					all_leads1.append(i)
		desc={i['parent']:[i['description'],i.get("next_follow_up_by") or "",i.get("mode_of_communication") or ""] for i in all_leads1}


		leads = [i['parent'] for i in all_leads1]
		site_lead=leads
		lead_filter['name'] = ['in', site_lead]

		leads = frappe.db.get_all('Quotation', filters=lead_filter, fields=['name', 'customer_name as lead_name', 'status', ])

		for i in leads:
			i['description']=desc[i["name"]][0]
			i['next_followup_by']=desc[i["name"]][1]
			i['mode_of_communication']=desc[i["name"]][2]

			contact=frappe.get_all(
				"Contact",
					filters=[
					["Dynamic Link", "link_doctype", "=", 'Quotation'],
					["Dynamic Link", "link_name", "=", i['name']],
					["Contact Phone", 'is_primary_mobile_no', "=", 1]

					],
					fields=['`tabContact Phone`.phone'],
					order_by='`tabContact`.creation desc'
				)
			if contact:
				i['contact_number']=contact[0]['phone']

			i['name'] = f'''<button style=" font-size: 13px;  background-color: #000000;color: #ffffff;border-radius: 5px; height: 23px;" onclick='frappe.set_route("Form", "Quotation", "{i["name"]}" )'>
			{i["name"]}
			</button>'''
   
		data+=leads

	return data
	

