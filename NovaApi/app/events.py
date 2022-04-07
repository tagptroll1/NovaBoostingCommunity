from .db.tables import ensure_tables


def setup_events(app):
    @app.on_event("startup")
    async def startup_event():
        await ensure_tables()