from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base


class BooksORM(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(150))
    description: Mapped[str | None]
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id", ondelete="CASCADE"))
    available_copies: Mapped[int]
