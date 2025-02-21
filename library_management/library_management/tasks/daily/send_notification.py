import frappe
from frappe.model.docstatus import DocStatus

@frappe.whitelist()
def send_overdue_book_notification():

    # Get overdue loans
    overdue_loans = frappe.get_all(
        "Loan",
        {
            "status": "On Loan",
            "docstatus": DocStatus.submitted(),
            "overdue_date": ("<=", frappe.utils.today())
        },
        ["name", "member", "book", "return_date", "overdue_date"]
    )
    
    for overdue_loan in overdue_loans:
        # Update loan status to "Overdue"
        loan = frappe.get_doc("Loan", overdue_loan.name)
        loan.status = "Overdue"
        loan.save(ignore_permissions=True)

        member = frappe.get_doc("Member", loan.member)
        overdue_book = loan.book
        subject = f"Overdue Book: {overdue_book}"
        recipient = member.email
    
        message = f"""Dear {member.name},
        This is to remind you that the book '{overdue_book}' is overdue.
        Overdue Date: {loan.overdue_date}
        
        Therefore, we kindly urge you to return the book ASAP so that you can avoid additional fines.

        Regards,
        Library Team        
        """

        try:
            frappe.sendmail(
                subject=subject,
                message=message,
                recipients=recipient,
                bulk=True
            )
            frappe.logger().info(f"Notification sent to {recipient} for overdue book {overdue_book}")
        except Exception as e:
            frappe.logger().error(frappe.get_traceback(), f'Error sending notifcation for loan {overdue_loan.member.name}')
        
    frappe.logger().info("Overdue book notification sent!")
