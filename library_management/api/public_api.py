import frappe

@frappe.whitelist(allow_guest=True)
def get_books():
    """
    Fetch all records from Book doctype
    """
    try:
        books = frappe.get_all(
            "Book",
            filters={
                "status": "Available",
                "web_published": 1,
            },
            fields=[
                "name", "title", "author", "publisher", "isbn", 
                "image", "publish_date", "description", "status"
            ] 
        )
        return {"status": "success", "book": books}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "API Error")
        return {"status": "error", "message": str(e)}


@frappe.whitelist(allow_guest=True)
def get_book(name):
    """
    Fetch detailed record of Book doctype
    """
    try:
        published_books = frappe.get_all(
            "Book", 
            filters={
                "name": name,
                # "web_published": 1,
            },
            fields=[
                "name", "title", "author", "publisher", "isbn", 
                "image", "publish_date", "description", "status"
            ]
        )
    
        # book = frappe.get_doc("Book",name)
        return {
            "status": "success", 
            "book": published_books[0] if len(published_books) > 0 else None
        }
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "API Error")
        return {"status": "error", "message": str(e)}


@frappe.whitelist(allow_guest=True)
def get_member():
    user = frappe.session.user
    if not user:
        frappe.throw("Authorization required!")
    
    try:
        member = frappe.get_doc({
                "doctype": "Member",
                "member_user": user
        })
        return {"status": "success", "member": member}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "API Error")
        return {"status": "error", "message": str(e)}


# Author
@frappe.whitelist(allow_guest=True)
def get_authors():
    """
    Fetch detailed record of Author doctype
    """
    try:
        authors = frappe.get_all(
            "Author", fields=["*"]
        )
        return {"status": "success", "authors": authors}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "API Error")
        return {"status": "error", "message": str(e)}