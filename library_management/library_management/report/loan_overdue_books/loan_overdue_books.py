# Copyright (c) 2025, Sis I and contributors
# For license information, please see license.txt

# import frappe
from frappe import _


def execute(filters: dict | None = None):
	"""Return columns and data for the report.

	This is the main entry point for the report. It accepts the filters as a
	dictionary and should return columns and data. It is called by the framework
	every time the report is refreshed or a filter is updated.
	"""
	columns = get_columns()
	data = get_data()

	return columns, data


def get_columns() -> list[dict]:
	"""Return columns for the report.

	One field definition per column, just like a DocType field definition.
	"""
	return [
		{
			"label": _("Column 1"),
			"fieldname": "column_1",
			"fieldtype": "Data",
		},
		{
			"label": _("Column 2"),
			"fieldname": "column_2",
			"fieldtype": "Int",
		},
	]


def get_data() -> list[list]:
    """Return data for the report.

    The report data is a list of rows, with each row being a list of cell values.
    """
    frappe.query_reports["Loan Overdue Books"] = {
        "filters": [
            {
                "fieldname": "name",
                "label": "Loan",
                "fieldtype": "Data",
                "reqd": 1,
            },
            {
                "fieldname": "book",
                "label": "Book",
                "fieldtype": "Link",
                "options": "Book",
            }
        ]
    }
    print(frappe.query_reports["Loan Overdue Books"])
    return [
        ["Row 1", 1],
        ["Row 2", 2],
    ]
