from app.DB.db import db

class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.UUID(as_uuid=True), primary_key=True, unique=True, nullable=False,
                   server_default=db.text("uuid_generate_v4()"))
