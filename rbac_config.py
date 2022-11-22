from enum import Enum

class ROLES(str,Enum):
    END_USER = "END_USER",
    MODERATOR = "MODERATOR",
    ADMIN = "ADMIN",
    ROOT = "ROOT"

class RBACMaster:
    @staticmethod
    def checkHandler(cls,allowed_roles,incoming_role):
        print("RBAC Master")
        if incoming_role in allowed_roles:
            return True
        return False

class FastApiRBACMaster:
    def RBAC(self,allowed_roles,incoming_role):
        print(allowed_roles)
        print(incoming_role)
        if incoming_role == ROLES.ROOT:
            return True
        else:
            return RBACMaster.checkHandler(allowed_roles,incoming_role)