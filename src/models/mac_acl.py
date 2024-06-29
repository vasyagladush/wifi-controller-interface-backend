from sqlalchemy import PickleType
from sqlalchemy.ext.mutable import MutableSet
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base


class MACACL(Base):
    __tablename__ = "mac_acls"
    id: Mapped[int] = mapped_column(primary_key=True)
    macs: Mapped[set[str]] = mapped_column(MutableSet.as_mutable(PickleType), nullable=False, default=set)  # type: ignore
    # TODO: Verify macs work as intended
