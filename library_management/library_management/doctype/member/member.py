# Copyright (c) 2025, Sis I and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Member(Document):

    # Unique User
    def before_save(self):
        # Ensure that the user is unique
        self.validate_user()
        
        
    def validate_user(self):
        member_exists = frappe.db.exists(
            'Member',
            {
                'member_user': self.member_user
            }
        )

        if member_exists:
            frappe.throw('Duplicate member user not allowed!')