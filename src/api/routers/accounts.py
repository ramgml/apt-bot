from fastapi import APIRouter, Request

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


@router.put("/{account_id}", response_model=AccountResponse)
async def update_account(account_id: int, db: DbSession, request: Request):
    """
    Update account.

    Args:
        account_id (int): Account ID.
        db (DbSession): Database session.

    Returns:
        Updated account.
    """
    body = await request.json()
    print('body', body)
    account_repo = AccountRepository(db)
    result = await account_repo.update(account_id, **body)
    print('result', result)
    return result
