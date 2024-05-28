frappe.ui.form.on("Lead", {
    custom_view_follow_up_details: function(frm){
		let data=`<table style="font-size:14px; border:1px solid black;width:100%">

			<tr style="font-weight:bold; border:1px solid black; padding:5px;">
				<td style="border:1px solid black; padding:5px;">
				<center>
				    S.No
				</center>
				</td>
				<td style="border:1px solid black; padding:5px;">
				<center>
					Date
				</center>
				</td>
				<td style="border:1px solid black; padding:5px;">
				<center>
					Mode of Communication
				</center>
				</td>
				<td style="border:1px solid black; padding:5px;">
				<center>
					Followed By
				</center>
				</td>
				<td style="border:1px solid black; padding:5px;">
				<center>
					Description
				</center>
				</td>
			</tr>
		`
		frm.doc.custom_view_follow_up_details_copy.forEach(row => {
			data += `
			<tr style="border:1px solid black; padding:5px;">
				<td style="border:1px solid black; padding:5px;">
				<center>
					${row.idx || ""}
				</center>
				</td>
				<td style="border:1px solid black; padding:5px;">
				<center>
					${frappe.format(row.date, {fieldtype:'Date'})}
				</center>
				</td>
				<td style="border:1px solid black; padding:5px;">
				<center>
					${row.mode_of_communication || ""}
				</center>
				</td>
				<td style="border:1px solid black; padding:5px;">
				<center>
					${row.user_name || ""}
				</center>
				</td>
				<td style="border:1px solid black; padding:5px;">
				<center>
					${row.description || ""}
				</center>
				</td>
			</tr>
			`
		})
		data += `</table>`
		var d = new frappe.ui.Dialog({
			title: __("Follow Up Details"),
			size:"extra-large",
			fields : [
				{
					fieldname: 'html_data',
					fieldtype: "HTML"
				}
			]
			
		})
		d.show();
		$(d.get_field('html_data').wrapper).html(data) 
	}
})
frappe.ui.form.on("Follow-Up", {
	date:function(frm,cdt,cdn){
		let row = locals[cdt][cdn]
		if(row.date){
			for (var i in cur_frm.doc.custom_view_follow_up_details_copy) {
				var value = cur_frm.doc.custom_view_follow_up_details_copy[i]
				if (row.idx == value.idx){
					break
				}
				if(row.date < value.date){
					frappe.show_alert({message:`Row - ${row.idx} Date (<span style='color:red'>${moment(row.date).format('DD-MM-YYYY')}</span>) should not be earlier than Row - ${value.idx} Date (<span style='color:red'>${moment(value.date).format('DD-MM-YYYY')}</span>)`, indicator:'red'})
					row.date = ''
					break
				}
			}
		}
	},
	next_follow_up_date:function(frm,cdt,cdn){
		let row = locals[cdt][cdn]
		if(row.next_follow_up_date < row.date){
			frappe.show_alert({message:`Follow Up Date - <span style='color:red'>${moment(row.next_follow_up_date).format('DD-MM-YYYY')}</span> should not be earlier than Date -<span style='color:red'> ${moment(row.date).format('DD-MM-YYYY')}</span>`,indicator:'red'})
			row.next_follow_up_date = ''
		}
	}
})