from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base


class Network(Base):
    __tablename__ = "networks"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    ssid: Mapped[str] = mapped_column(nullable=True)
    country_code: Mapped[str] = mapped_column(String(2), nullable=False)
    access_points: Mapped[list["AccessPoint"]] = relationship(
        "AccessPoint",
        secondary="ap_network_connectors",
        back_populates="networks",
        lazy="selectin",
    )


from models.access_point import AccessPoint
