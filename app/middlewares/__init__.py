from .throttling import ThrottlingMiddleware
from app.loader import dp


if __name__ == "middlewares":
    dp.middleware.setup(ThrottlingMiddleware())
