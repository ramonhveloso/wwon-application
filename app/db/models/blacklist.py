from sqlalchemy import Column, String, DateTime
from datetime import datetime, timezone
from app.db.base import Base

class TokenBlacklist(Base):
    __tablename__ = "token_blacklist"

    id = Column(String, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc)) 
