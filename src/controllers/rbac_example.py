from fastapi import APIRouter, Depends

from src.models.user import UserRole
from src.utils.rbac import get_current_user, has_role

router = APIRouter(tags=["RBAC Example"])


@router.get("/public")
async def public_endpoint():
    """
    Endpoint accessible to everyone, no authentication required
    """
    return {"message": "This is a public endpoint"}


@router.get("/authenticated")
async def authenticated_endpoint(current_user: dict = Depends(get_current_user)):
    """
    Endpoint accessible to any authenticated user
    """
    return {
        "message": "This is an authenticated endpoint",
        "user_id": current_user["id"],
        "user_email": current_user["email"],
        "user_role": current_user["role"],
    }


@router.get("/admin-only")
async def admin_only_endpoint(
    current_user: dict = Depends(has_role(UserRole.administrador)),
):
    """
    Endpoint accessible only to administrators
    """
    return {
        "message": "This is an admin-only endpoint",
        "user_id": current_user["id"],
        "user_email": current_user["email"],
    }


@router.get("/staff-only")
async def staff_only_endpoint(
    current_user: dict = Depends(
        has_role([UserRole.administrador, UserRole.cajero, UserRole.cocinero])
    )
):
    """
    Endpoint accessible to staff members
    """
    return {
        "message": "This is a staff-only endpoint",
        "user_id": current_user["id"],
        "user_email": current_user["email"],
        "user_role": current_user["role"],
    }
