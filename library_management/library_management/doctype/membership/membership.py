# Copyright (c) 2025, Sis I and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.docstatus import DocStatus


class Membership(Document):
    
    def before_save(self):
        # Get the membership period and compute the end date by adding the start date and the membership period
        membership_period = frappe.db.get_single_value('Library Settings', 'membership_period')
        self.end_date = frappe.utils.add_days(self.start_date, membership_period)
    

    # Before submitting the document, check if the member is already a member
    def before_submit(self):
        # Check if the member is already a member
        is_active_member = frappe.db.exists(
            'Membership',
            {
                'member': self.member,
                'docstatus': DocStatus.submitted(),
                # Check if membership end date is greater than start date
                'end_date': ('>', self.start_date),
                'status': 'Active',
            }
        )

        # If the member is already a member, throw an error	if is_member:
        if is_active_member:
            frappe.throw('This member is already an active member')	
