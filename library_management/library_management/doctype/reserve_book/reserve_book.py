# Copyright (c) 2025, Sis I and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.docstatus import DocStatus


class ReserveBook(Document):

    def before_save(self):
        if not self.reserve_date:
            self.reserve_date = frappe.utils.today()

        self.validate_member_book_loan()


    def before_submit(self):
        if self.status == 'Active':
            self.validate_membership()
            self.validate_book_is_reserved()

    # def on_cancel(self):
    #     self.status = 'Cancelled'
    #     self.save()

    def validate_member_book_loan(self):
        loan_exists = frappe.db.exists(
            'Loan',
            {
                'member': self.member,
                'book': self.book,
                'status': 'On Loan',
                'docstatus': DocStatus.submitted()
            }
        )

        if loan_exists:
            frappe.throw('Member has already loaned the book!')


    def validate_book_is_reserved(self):
        reserve_exists = frappe.db.exists(
            'Reserve Book',
            {
                'member': self.member,
                'book': self.book,
                'docstatus': DocStatus.submitted(),
                'status': 'Active'
            }
        )

        if reserve_exists:
            frappe.throw('Book is already reserved!')
    
    def validate_membership(self):
        # Check for active membership
        active_membership = frappe.db.exists (
            'Membership',
            {
                'member': self.member,
                'status': 'Active',
                'docstatus': DocStatus.submitted(),
                'start_date': ('<=', self.reserve_date),
            }
        )

        if not active_membership:
            frappe.throw('No valid/Active membership found to this member!')