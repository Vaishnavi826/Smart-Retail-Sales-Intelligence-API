

from app.database import engine
from app.models import Base

# Create all database tables
Base.metadata.create_all(bind=engine)

print("Database tables created successfully!")
