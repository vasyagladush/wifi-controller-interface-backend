from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base


class Wireless(Base):
    __tablename__ = "wireless"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    vht: Mapped[bool] = mapped_column(default=False)
    acs: Mapped[bool] = mapped_column(default=False)
    beacon_interval: Mapped[int] = mapped_column(nullable=False)
    rts_cts_threshold: Mapped[int] = mapped_column(
        nullable=False
    )  # Backend must verify range 1 - 65535
    networks: Mapped[list["Network"]] = relationship(
        "Network",
        secondary="network_wireless_connectors",
        back_populates="wireless",
        lazy="selectin",
    )


from models.network import Network
