from fastapi import APIRouter, Depends, HTTPException, status

from core.business.auth.login_user_port import LoginUserPort
from core.business.auth.register_user_port import RegisterUserPort
from core.context import Context
from domain.exceptions.business_exception import BusinessException
from domain.user.user import User
from web.commons.api_response import ApiResponse
from web.dependencies import (
    get_current_user,
    get_login_user_port,
    get_register_user_port,
)
from web.mappers.user_model_mapper import UserModelMapper
from web.models.request.auth.login_request import LoginRequest
from web.models.request.auth.register_request import RegisterRequest
from web.models.response.auth.auth_response import AuthResponse
from web.models.response.user.user_response import UserResponse

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

_user_mapper = UserModelMapper()


@router.post(
    "/register",
    response_model=ApiResponse[UserResponse],
    status_code=status.HTTP_201_CREATED,
)
async def register(
    body: RegisterRequest,
    register_port: RegisterUserPort = Depends(get_register_user_port),
):
    context = Context(data=User(name=body.name, email=body.email))
    context.put_property("password", body.password)

    try:
        user = await register_port.execute(context)
    except BusinessException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return ApiResponse.success(
        data=_user_mapper.to_response(user),
        message="Usuário cadastrado com sucesso",
    )


@router.post("/login", response_model=ApiResponse[AuthResponse])
async def login(
    body: LoginRequest,
    login_port: LoginUserPort = Depends(get_login_user_port),
):
    context = Context()
    context.put_property("email", body.email)
    context.put_property("password", body.password)

    try:
        auth_token = await login_port.execute(context)
    except BusinessException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    user = context.get_property("user", User)

    return ApiResponse.success(
        data=AuthResponse(
            access_token=auth_token.access_token,
            token_type=auth_token.token_type,
            expires_at=auth_token.expires_at,
            user=_user_mapper.to_response(user),
        ),
        message="Login realizado com sucesso",
    )


@router.get("/me", response_model=ApiResponse[UserResponse])
async def me(user: User = Depends(get_current_user)):
    return ApiResponse.success(data=_user_mapper.to_response(user))
