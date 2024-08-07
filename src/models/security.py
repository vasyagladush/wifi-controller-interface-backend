import enum

from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base

# TODO: Move enums into another file(s)?
# TODO: Verify this works with sqlite


# WirelessSecurityType:
# NO_PROTECTION = 0
# WEP = 1
# WPA_PSK = 2
# WPA_ENTERPRISE = 3
# WPA2_PSK = 4
# WPA2_ENTERPRISE = 5
# WPA3_PSK = 6
# WPA3_ENTERPRISE = 7


# ACLType:
# OFF = 0
# DENY = 1
# PERMIT = 2


class SecurityMACACLConnector(Base):
    __tablename__ = "security_mac_acl_connectors"
    id: Mapped[int] = mapped_column(primary_key=True)
    security_id: Mapped[int] = mapped_column(ForeignKey("security.id"))
    mac_acl_id: Mapped[int] = mapped_column(ForeignKey("mac_acls.id"))


class Security(Base):
    __tablename__ = "security"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    wireless_security_type: Mapped[int] = mapped_column(default=0)
    radius: Mapped[str] = mapped_column(nullable=True)
    eap: Mapped[bool] = mapped_column(default=False)
    mac_acl_type: Mapped[int] = mapped_column(default=0)
    mac_acls: Mapped[list["MACACL"]] = relationship(
        "MACACL",
        secondary="security_mac_acl_connectors",
        back_populates="security",
        lazy="selectin",
    )
    networks: Mapped[list["Network"]] = relationship(
        "Network",
        secondary="network_security_connectors",
        back_populates="security",
        lazy="selectin",
    )


from models.mac_acl import MACACL
from models.network import Network
