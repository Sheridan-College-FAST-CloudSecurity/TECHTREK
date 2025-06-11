from app.database import Base, engine
from app import models  # This ensures tables are loaded

print("Creating tables in test.db...")
Base.metadata.create_all(bind=engine)
print("Done.")
