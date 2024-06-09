from uuid import uuid4

from sqlalchemy.orm import declarative_base

Base = declarative_base()

from models.AP import AP, AP_Network_Connector
from models.network import Network
from models.user import User
