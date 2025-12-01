from fastapi import APIRouter

from api.dependencies import DbSession
from api.schemas.accounts import AccountResponse
from repositories.accounts import AccountRepository
from repositories.user import UserRepository


router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.get("/", response_model=list[AccountResponse])
async def get_user_accounts(db: DbSession):
    """
    Get user accounts list.

    Args:
        db (DbSession): Database session.

    Returns:
        List of user accounts.
    """
    user_id = 3
    user_repo = UserRepository(db)
    user = await user_repo.get_by_id(user_id)

    if user:
        account_repo = AccountRepository(db)
        return await account_repo.get_by_user(user)

    return []
