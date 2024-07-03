from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base


class NetworkWirelessConnector(Base):
    __tablename__ = "network_wireless_connectors"
    id: Mapped[int] = mapped_column(primary_key=True)
    network_id: Mapped[int] = mapped_column(ForeignKey("networks.id"))
    wireless_id: Mapped[int] = mapped_column(ForeignKey("wireless.id"))


class NetworkSecurityConnector(Base):
    __tablename__ = "network_security_connectors"
    id: Mapped[int] = mapped_column(primary_key=True)
    network_id: Mapped[int] = mapped_column(ForeignKey("networks.id"))
    security_id: Mapped[int] = mapped_column(ForeignKey("security.id"))


class Network(Base):
    __tablename__ = "networks"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    ssid: Mapped[str] = mapped_column(nullable=True)
    country_code: Mapped[str] = mapped_column(String(2), nullable=False)
    password: Mapped[str] = mapped_column(
        String, nullable=True
    )  # ENCRYPTED, not plain text !!!
    access_points: Mapped[list["AccessPoint"]] = relationship(
        "AccessPoint",
        secondary="ap_network_connectors",
        back_populates="networks",
        lazy="selectin",
    )
    wireless: Mapped[list["Wireless"]] = relationship(
        "Wireless",
        secondary="network_wireless_connectors",
        back_populates="networks",
        lazy="selectin",
    )
    security: Mapped[list["Security"]] = relationship(
        "Security",
        secondary="network_security_connectors",
        back_populates="networks",
        lazy="selectin",
    )


from models.access_point import AccessPoint
from models.security import Security
from models.wireless import Wireless
