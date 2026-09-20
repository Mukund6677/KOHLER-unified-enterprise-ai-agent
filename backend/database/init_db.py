from .db import engine, Base
from .models import Employee

Base.metadata.create_all(bind=engine)

print("KOHLER database created successfully.")