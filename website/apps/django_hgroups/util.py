class AuthBackend:

    def authenticate(self, username=None, password=None):
        return None

    def get_group_permissions(self, user_obj):
        groups = user_obj.get_all_groups()
        permissions = set()
        for group in groups:
            for perm in group.permissions.all():
                permissions.add(perm.codename)
        return list(permissions)

    def get_all_permissions(self, user_obj):
        return self.get_group_permissions(user_obj)

    def has_perm(self, user_obj, perm):
        permissions = self.get_all_permissions(user_obj)
        for p in permissions:
            if p == perm:
                return True
        return False

    def has_perms(self, user_obj, perm_list):
        for perm in perm_list:
            if not self.has_perm(user_obj, perm):
                return False
        return True
