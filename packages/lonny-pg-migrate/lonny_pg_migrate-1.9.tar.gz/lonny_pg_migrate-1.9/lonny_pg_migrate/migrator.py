from .cfg import Configuration
from .logger import logger
from datetime import datetime

class Migrator:
    def __init__(self, db):
        self._db = db
    
    def migrate(self, * migrations):
        logger.info("Ensuring migration table is created.")
        self._db.execute(lambda o: f"""
            CREATE TABLE IF NOT EXISTS {Configuration.table} (
                slug TEXT NOT NULL,
                run_dt TIMESTAMP NOT NULL,
                PRIMARY KEY (slug)
            )
        """)

        for slug, migration in migrations:
            logger.info(f"Performing migration: {slug}.")
            row = self._db.fetch_one(lambda o: f"""
                SELECT 1 FROM {Configuration.table}
                WHERE slug = {o(slug)}
            """)
            if row is not None:
                logger.debug("Migration already exists - skipping.")
                continue

            migration(self._db)
            self._db.execute(lambda o: f"""
                INSERT INTO {Configuration.table} VALUES (
                    {o(slug)},
                    {o(datetime.utcnow())}
                )
            """)

    def drop(self):
        logger.info("Dropping schema.")
        self._db.execute("DROP SCHEMA public CASCADE")
        self._db.execute("CREATE SCHEMA public")
        self._db.execute("GRANT ALL ON SCHEMA public TO postgres")
        self._db.execute("GRANT ALL ON SCHEMA public TO public")