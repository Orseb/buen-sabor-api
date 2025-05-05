from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context
from src.config.database import DATABASE_URL

# Models import
from src.models.base import BaseModel
from src.models.inventory_item import InventoryItemModel  # noqa
from src.models.inventory_item_category import InventoryItemCategoryModel  # noqa
from src.models.manufactured_item_category import ManufacturedItemCategoryModel  # noqa
from src.models.measurement_unit import MeasurementUnitModel  # noqa
from src.models.user import UserModel  # noqa

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = BaseModel.metadata
config.set_main_option("sqlalchemy.url", DATABASE_URL)


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
