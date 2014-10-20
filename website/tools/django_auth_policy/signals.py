from django import dispatch

# user_expired is send as soon as a user expires
# It can be used to inform the user or an admin about the expiry
user_expired = dispatch.Signal(providing_args=["user"])

# temporary_password_set is send when a user gets a temporary password
# It can be used to inform the user about the temporary password
temporary_password_set = dispatch.Signal(providing_args=["user", "request",
                                                         "password"])
