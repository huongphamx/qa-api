# Import all the models, so that Alembic can read from memory
# and auto generate migration
# https://stackoverflow.com/questions/15660676/alembic-autogenerate-producing-empty-migration
from app.db.base_model import Base
from app.models.lecturer import Lecturer
