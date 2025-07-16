import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# --- بداية التعديل ---

# إضافة المسار الجذر للمشروع حتى يتمكن Alembic من العثور على وحدة src
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), "..")))

# استيراد كائن Base من ملف النماذج الخاص بك
from src.alsaada_bot.database import Base

# --- نهاية التعديل ---


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- بداية التعديل ---

# قم بتعيين الـ metadata هنا
target_metadata = Base.metadata

# --- نهاية التعديل ---

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
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
    """Run migrations in 'online' mode."""
    # --- التعديل الوحيد هنا ---
    # استبدال المتغير الخاطئ config.config_section_name
    # بالاسم الصحيح للقسم وهو "alembic"
    connectable = engine_from_config(
        config.get_section("alembic", {}),
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