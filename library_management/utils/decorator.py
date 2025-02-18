import frappe


# Decorator for permission requirement
def permission_required(roles):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not has_roles(roles):
                frappe.throw("You have no permission!")
            return func(*args, **kwargs)
        
        return wrapper
    return decorator


# Permission Role check
def has_roles(required_roles):
    """
    Check if user has a required role
    """
    user = frappe.session.user

    if not user:
        frappe.throw("Authontication required!")

    user_roles = frappe.get_roles(user)
    return any(role in user_roles for role in required_roles)