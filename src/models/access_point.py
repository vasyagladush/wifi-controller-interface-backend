from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base


class APNetworkConnector(Base):
    __tablename__ = "ap_network_connectors"
    id: Mapped[int] = mapped_column(primary_key=True)
    access_point_id: Mapped[int] = mapped_column(
        ForeignKey("access_points.id")
    )
    network_id: Mapped[int] = mapped_column(ForeignKey("networks.id"))


class AccessPoint(Base):
    __tablename__ = "access_points"
    id: Mapped[int] = mapped_column(primary_key=True)
    device_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    name: Mapped[str] = mapped_column(unique=True)
    ip: Mapped[str] = mapped_column(nullable=False)
    networks: Mapped[list["Network"]] = relationship(
        "Network",
        secondary="ap_network_connectors",
        back_populates="access_points",
        lazy="joined",
    )


from models.network import Network
