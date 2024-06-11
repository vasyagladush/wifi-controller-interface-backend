from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.network import Network

from . import Base


class AccessPoint(Base):
    __tablename__: str = "access_points"
    id: Mapped[int] = mapped_column(primary_key=True)
    device_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    name: Mapped[str] = mapped_column(unique=True)
    networks: Mapped[list] = relationship(
        Network, secondary="ap_network_connector"
    )


class APNetworkConnector(Base):
    __tablename__: str = "ap_network_connectors"
    id: Mapped[int] = mapped_column(primary_key=True)
    acess_point_id: Mapped[int] = mapped_column(ForeignKey(AccessPoint.id))
    network_id: Mapped[int] = mapped_column(ForeignKey(Network.id))