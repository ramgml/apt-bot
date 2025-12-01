from fastapi import APIRouter

from api.dependencies import DbSession
from api.schemas.users import UserResponse
from repositories.user import UserRepository


router = APIRouter(prefix="/users", tags=["profile"])


@router.get("/", response_model=UserResponse)
async def get_user(db: DbSession):
    # TODO: заменить на получения пользователя по токену
    user_id = 3
    user_repo = UserRepository(db)
    user = await user_repo.get_by_id(user_id)
    return user
