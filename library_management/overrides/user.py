import frappe

def assign_roles_to_new_user(doc, method=None):
    """
    Assign roles to newly created Website Users
    """

    if doc.user_type == "Website User":
        # Create a new member user
        member = frappe.get_doc({
            "doctype": "Member",
            "member_name": doc.full_name, # Use user full name
            "email": doc.email, # Link to user email
            "member_user": doc.name # Link to the name field of user i.e email
        })
        member.insert(ignore_permissions=True)
        
        # Assign the "Member" role to the user
        role = "Member"
        role_exists = frappe.db.exists(
            "Has Role", {
                "parent": doc.name,
                "role": role
            }
        )
        if not role_exists:
            doc.append("roles", {"role": role})
        
        doc.save(ignore_permissions=True)

