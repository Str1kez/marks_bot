from .is_group import IsGroup
from app.loader import dp


if __name__ == "filters":
    dp.filters_factory.bind(IsGroup)
