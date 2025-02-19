import frappe

# Request for book loan
@frappe.whitelist(allow_guest=True)
def request_book_loan(book_name):
    user = frappe.session.user
    
    if not user:
        frappe.throw("User must be logged in for this request!")
    
    try:
        book = frappe.get_doc("Book", book_name)
        book_status = book.status
        if book_status != "Available":
            return {
                "status": "warning", 
                "message": "Book is not available for loan!",
                "book_status": book_status
            }
        
        member = frappe.get_doc("Member", {"member_user": user})
        loan_exists = frappe.db.exists({
            "doctype": "Loan",
            "book": book_name,
            "member": member.name
        })

        if loan_exists:
            return {"status": "warning", "message": "You have already requested or borrowed this book!"}
        
        loan = frappe.new_doc("Loan")
        loan.book = book_name
        loan.member = member.name
        # laon.status = "Draft"
        loan.save(ignore_permissions=True)
        
        return {"status": "success", "message": "Book loan request successful!"}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "API Error")
        return {"status": "error", "message": str(e)} 
  