from sqlalchemy import PickleType
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base


class MACACL(Base):
    __tablename__ = "mac_acls"
    id: Mapped[int] = mapped_column(primary_key=True)
    macs: Mapped[list[str]] = mapped_column(MutableList.as_mutable(PickleType), nullable=False, default=[])  # type: ignore
    # TODO: Verify macs work as intended
    security: Mapped[list["Security"]] = relationship(
        "Security",
        secondary="security_mac_acl_connectors",
        back_populates="mac_acls",
        lazy="selectin",
    )


from models.security import Security
