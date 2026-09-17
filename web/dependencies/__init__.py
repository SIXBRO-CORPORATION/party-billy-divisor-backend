from web.dependencies.persistence_dependencies import (
    get_user_repository,
    get_bill_repository,
)

from web.dependencies.security_dependencies import (
    get_jwt_provider,
    get_password_hasher,
    get_current_user_id,
    get_current_user,
)

from web.dependencies.business.auth_dependencies import (
    get_register_user_port,
    get_login_user_port,
)
