from sqlalchemy.orm import sessionmaker
from database import engine          # the engine from Chapter 13
SessionLocal = sessionmaker(bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db                      # hand the connection to the endpoint
    finally:
        db.close()                    # ... and always close it afterwards
