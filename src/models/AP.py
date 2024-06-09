from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.network import Network

from . import Base


class AP(Base):
    __tablename__: str = "ap"
    id: Mapped[int] = mapped_column(primary_key=True)
    device_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    name: Mapped[str] = mapped_column(unique=True)
    networks: Mapped[list] = relationship(
        Network, secondary="ap_network_connector"
    )


class AP_Network_Connector(Base):
    __tablename__: str = "ap_network_connector"
    id: Mapped[int] = mapped_column(primary_key=True)
    ap_id: Mapped[int] = mapped_column(ForeignKey(AP.id))
    network_id: Mapped[int] = mapped_column(ForeignKey(Network.id))
