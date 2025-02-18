import frappe

import json

from ..utils.decorator import permission_required

# SIS -I OR Admin Auth
# API Secret: b4349bc0e92ef30
# API KEY: 29f87047e6ec401

# Test in Bruno
# Header
# Authoriztion : token 29f87047e6ec401:b4349bc0e92ef30


# Test for: lib2@library.sys
# API Secret: 9a5b88279574a39
# API Key: 1eee8d81de80914
# Authorization: token 1eee8d81de80914:9a5b88279574a39


@frappe.whitelist()
@permission_required(["Admin", "Librarian"])
def get_all_book(fields=None, **kwargs):
    """
    Fetch all records from Book doctype
    """
    try:
        books = frappe.get_all(
            "Book",
            fields=fields if fields else ["*"]
        )
        return {"status": "success", "book": books}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "API Error")
        return {"status": "success", "message": str(e)}


@frappe.whitelist()
@permission_required(["Admin", "Librarian"])
def get_detail_book(name, **kwargs):
    """
    Fetch detailed record of Book doctype
    """
    try:
        book = frappe.get_doc("Book",name)
        return {"status": "success", "book": book}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "API Error")
        return {"status": "error", "message": str(e)}


@frappe.whitelist()
@permission_required(["Admin", "Librarian"])
def create_book(
        title, author, isbn=None, published_date=None, 
        publisher=None, image=None, total_copies=1, web_published=0, **kwargs):
    """
    Create new book
    """
    book = frappe.get_doc({
        "doctype": "Book",
        "title": title,
        "author": author,
        "isbn": isbn,
        "published_date": published_date,

    })
    book.insert()
    return {"status": "success", "message": f"New book name '{book.name}' was created successfully!"}


@frappe.whitelist()
@permission_required(roles=["Admin", "Librarian"])
def update_book(name, **kwargs):
    """
    Update a book record
    """
    data = json.loads(frappe.request.data)
    try:
        book = frappe.get_doc("Book", name)

        for fieldname, value in data.items():
            if fieldname in book.meta.get_valid_columns():
                book.set(fieldname, value)

        book.save(ignore_permissions=False)

        return {"status": "success", "message": "Book updated successfully"}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "API Error for Update")
        return {"status": "error", "message": str(e)}


@frappe.whitelist()
@permission_required(roles=["Admin"])
def delete_book(name, **kwargs):
    """
    Delete a book record
    """
    try:
        book = frappe.get_doc("Book", name)
        book.delete()
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "API Error for delete")
        return {"status": "error", "message": str(e)}


@frappe.whitelist()
@permission_required(roles=["Admin", "Librarian"])
def get_members(fields=None, **kwargs):
    """
    Retrieve List of members, if user wishes to get specific fields 
    using these notations 'fields=["field1", "field2", ...]' or 'fields["*"]' to see all fields
    """
    try:
        members = frappe.get_all(
            "Member",
            fields=fields if fields else ["*"]
        )
        return {"status": "success", "members": members}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "API Error")
        return {"status": "success", "message": str(e)}


@frappe.whitelist()
@permission_required(roles=["Admin", "Librarian"])
def get_member(name, **kwargs):
    """
    Retreive single member
    """
    try:
        member = frappe.get_doc("Member", name)
        return {"status": "success", "member": member}
    except Exception as e:
        frappe.log_error(frappe.get_tracebackk(), "API Error")
        return {"status": "error", "message": str(e)}


@frappe.whitelist()
@permission_required(roles=["Admin", "Librarian"])
def create_member(member_user, **kwargs):
    """
    Create new member
    """
    member = frappe.get_doc({
        "doctype": "Member",
        "member_user": member_user,
    })
    member.insert()
    return {
        "status": "success", 
        "message": f"New member '{member.name}' was created successfully!"
    }


@frappe.whitelist()
@permission_required(roles=["Admin", "Librarian"])
def update_member(name, **kwargs):
    """
    Update a member record
    """
    data = json.loads(frappe.request.data)
    try:
        member = frappe.get_doc("Member", name)

        for fieldname, value in data.items():
            if fieldname in member.meta.get_valid_columns():
                member.set(fieldname, value)

        member.save(ignore_permissions=False)

        return {"status": "success", "message": "Member updated successfully"}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "API Error for Update")
        return {"status": "error", "message": str(e)}


@frappe.whitelist()
@permission_required(roles=["Admin"])
def delete_member(name, **kwargs):
    """
    Delete a member
    """
    try:
        member = frappe.get_doc("Member", name)
        member.delete()
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "API Error for delete")
        return {"status": "error", "message": str(e)}

