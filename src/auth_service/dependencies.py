from fastapi import Depends, HTTPException, status

from src.auth_service.models import UserRole
from src.auth_service.services.auth_service import get_current_user


def require_role(role: UserRole):
    def dependency(user=Depends(get_current_user)):
        if user.role != role:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Insufficient permissions')
        return user
    return dependency
