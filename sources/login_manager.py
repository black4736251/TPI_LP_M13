from sources.database import check_login, get_user, fetch_all


class LoginResult:
    def __init__(self, success, error=None, user=None, role=None, stock_data=None) -> None:
        self.success = success
        self.error = error
        self.user = user
        self.role = role
        self.stock_data = stock_data


class LoginManager:
    _instance: "LoginManager | None" = None


    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance


    def login(self, username: str, password: str) -> LoginResult:
        username = username.strip()
        password = password.strip()

        # Empty fields
        if not username or not password:
            return LoginResult(
                success=False,
                error="empty_fields"
            )

        # Invalid credentials
        if not check_login(username, password):
            return LoginResult(
                success=False,
                error="invalid_credentials"
            )

        # Valid login
        user = get_user(username)

        # Just in case something goes wrong for user
        if user is None:
            return LoginResult(success=False, error="invalid_credentials")

        role = user["role"]

        stock_data = fetch_all() if role == "admin" else None

        return LoginResult(
            success=True,
            user=user,
            role=role,
            stock_data=stock_data
        )