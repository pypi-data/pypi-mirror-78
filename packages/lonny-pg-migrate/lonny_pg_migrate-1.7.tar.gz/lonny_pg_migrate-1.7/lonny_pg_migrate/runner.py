from .cfg import Configuration
from functools import wraps
from .logger import logger
from datetime import datetime

class Migration:
    def __init__(self, slug, sort_key, fn):
        self.slug = slug
        self.sort_key = sort_key
        self._fn = fn

    def __call__(self, *args, **kwargs):
        return self._fn(*args, **kwargs)

class MigrationRunner():
    def __init__(self, db):
        self._db = db
        self._data = dict()

    def migration(self, slug, ** kwargs):
        def wrapper(fn):
            sort_key = kwargs.get("sort_key", slug)
            migration = wraps(fn)(Migration(slug, sort_key, fn))
            self._data[slug] = migration
            return migration
        return wrapper

    def _create(self):
        logger.info("Ensuring migration table is created.")
        self._db.execute(lambda o: f"""
            CREATE TABLE IF NOT EXISTS {Configuration.table} (
                slug TEXT NOT NULL,
                run_dt TIMESTAMP NOT NULL,
                PRIMARY KEY (slug)
            )
        """)

    def _write_migration(self, slug):
        self._db.execute(lambda o: f"""
            INSERT INTO {Configuration.table} VALUES (
                {o(slug)},
                {o(datetime.utcnow())}
            )
        """)

    def _check_migration_exists(self, slug):
        row = self._db.fetch_one(lambda o: f"""
            SELECT 1 FROM {Configuration.table}
            WHERE slug = {o(slug)}
        """)
        return row is not None

    def _get_migrations(self):
        return sorted(self._data.values(), key = lambda x: x.sort_key)

    def migrate(self):
        self._create()
        for migration in self._get_migrations():
            logger.info(f"Performing migration: {migration.slug} @ {migration.sort_key}.")
            if self._check_migration_exists(migration.slug):
                logger.debug("Migration already exists - skipping.")
                continue
            migration(self._db)
            self._write_migration(migration.slug)

    def drop(self):
        logger.info("Dropping schema.")
        self._db.execute("DROP SCHEMA public CASCADE")
        self._db.execute("CREATE SCHEMA public")
        self._db.execute("GRANT ALL ON SCHEMA public TO postgres")
        self._db.execute("GRANT ALL ON SCHEMA public TO public")