from application.database import engine
from application.models import Base

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

engine.dispose()
