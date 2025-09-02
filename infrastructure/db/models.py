from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Text, ForeignKey, DateTime, func


class Base(DeclarativeBase):
    pass


class UserModel(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped["DateTime"] = mapped_column(DateTime(timezone=True), server_default=func.now())
    resumes = relationship("ResumeModel", back_populates="user", cascade="all, delete-orphan")


class ResumeModel(Base):
    __tablename__ = "resumes"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped["DateTime"] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped["DateTime"] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    user = relationship("UserModel", back_populates="resumes")
    improvements = relationship("ResumeImprovementModel", back_populates="resume", cascade="all, delete-orphan")


class ResumeImprovementModel(Base):
    __tablename__ = "resume_improvements"
    id: Mapped[int] = mapped_column(primary_key=True)
    resume_id: Mapped[int] = mapped_column(ForeignKey("resumes.id", ondelete="CASCADE"), index=True, nullable=False)
    original_content: Mapped[str] = mapped_column(Text)
    improved_content: Mapped[str] = mapped_column(Text)
    created_at: Mapped["DateTime"] = mapped_column(DateTime(timezone=True), server_default=func.now())
    resume = relationship("ResumeModel", back_populates="improvements")