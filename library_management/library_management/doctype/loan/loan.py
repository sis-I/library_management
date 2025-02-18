# Copyright (c) 2025, Sis I and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.docstatus import DocStatus


class Loan(Document):
    def before_save(self):
        # Ensure loan date is not past date
        # if self.loan_date < frappe.utils.today():
        #     frappe.throw("Loan date cannot be a past date!")

        # Ensure that return date do not exceed max loan days
        # self.validate_max_loan_days()

        loan_period = frappe.db.get_single_value('Library Settings', 'loan_period')
        self.overdue_date = frappe.utils.add_days(self.loan_date, loan_period + 1)

    def before_submit(self):
        self.validate_status()
    

    def before_update_after_submit(self):
        # Apply validation if the loan status is changed
        # self.validate_status()
        pass

    def validate_status(self):
        """
        Validate the loan based on workflow status e.i. On Loan, Returned, Overdue
        """
        if self.status == 'On Loan':
            self.validate_onloan()
            book = frappe.get_doc('Book', self.book)
            book.available_copies -= 1

            if book.available_copies < 1:
                book.status = 'On Loan'

            book.save()

        elif self.status == 'Returned':
            self.validate_returned()

            book = frappe.get_doc('Book', self.book)
            book.available_copies += 1

            # Only change the statu to 'Available' if all copies are returned
            if book.status == 'On Loan':
                book.status = 'Available'
            book.save()

        elif self.status == 'Overdue':
            pass

    def validate_onloan(self):
        # Check for memebership validation
        self.validate_membership()

        self.validate_max_limit()

        book = frappe.get_doc('Book', self.book)

        # Check if the book is already on loan
        if book.status == 'On Loan':
            frappe.throw('Book is already on loan!')

    def validate_returned(self):
        book = frappe.get_doc('Book', self.book)

        loan_exists = frappe.db.exists(
            'Loan',
            {
                'book': self.book,
                'member': self.member,
                'status': 'On Loan',
                'docstatus': DocStatus.submitted()
            }
        )
        
        if not loan_exists:
            frappe.throw('No active book loan found for the member!')

        if book.available_copies == book.total_copies:
            frappe.throw('All copies of the book are already returned!')

    def validate_overdue(self):
        pass

    def validate_lost(self):
        pass
    
    def validate_membership(self):
        active_membership = frappe.db.exists(
            'Membership',
            {
                'member': self.member,
                'docstatus': DocStatus.submitted(),
                'status': 'Active',
                'end_date': ('>=', self.loan_date),
                'start_date': ('<=', self.loan_date),
            }
        )

        print("Membership", active_membership)

        if not active_membership:
            frappe.throw('No valid/active membership found for the member!')
    
    def validate_max_loan_days(self):
        # Check if return date exceeds the max loan peroiod
        max_loan_days = frappe.db.get_single_value('Library Settings', 'loan_period')
        loan_date_diff = frappe.utils.date_diff(self.return_date, self.loan_date)

        if loan_date_diff > max_loan_days:
            frappe.throw('Return date exceeds the maximum loan period!')


    def validate_max_limit(self):
        max_books = frappe.db.get_single_value('Library Settings', 'max_books')
        borrowed_books = frappe.db.count(
            'Loan',
            {
                'member': self.member,
                'status': 'On Loan',
                'docstatus': DocStatus.submitted()
            }
        )

        if borrowed_books >= max_books:
            frappe.throw('Maximum limit of books reached for the member!')

