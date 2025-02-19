# Copyright (c) 2025, Sis I and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator


class Book(WebsiteGenerator):

    def before_save(self):
        if not self._doc_before_save:
            self.available_copies = self.total_copies

        if self.total_copies < 1:
            frappe.throw('Total copies should be at least 1!')

    def on_update(self):

        if self.available_copies < 0:
            frappe.throw('Available copies must not be negative!')
        elif self.available_copies > self.total_copies:
            frappe.throw('Available copies must not exceed total copies!')