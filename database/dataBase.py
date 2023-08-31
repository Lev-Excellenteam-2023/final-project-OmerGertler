from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import uuid
import os
from enum import Enum as PyEnum
from datetime import datetime

# Define a SQLite Database and ORM Base
Base = declarative_base()


# ENUM for Upload Status
class UploadStatus(PyEnum):
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    DONE_SUCCESS = 'done_success'
    DONE_WITH_ERRORS = 'done_with_errors'
    FAILED = 'failed'


# Define ORM Classes for Users and Uploads Tables
class User(Base):
    """Class representing the 'users' table in the database."""

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False, unique=True)

    uploads = relationship('Upload', back_populates='user', cascade='all, delete-orphan')


class Upload(Base):
    """Class representing the 'uploads' table in the database."""

    __tablename__ = 'uploads'
    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(String, default=str(uuid.uuid4()), unique=True)
    filename = Column(String)
    upload_time = Column(DateTime, default=datetime.now)
    finish_time = Column(DateTime)
    status = Column(Enum(UploadStatus), default=UploadStatus.PENDING)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('User', back_populates='uploads', cascade='all')

    def upload_path(self) -> str:
        """Compute the path of the uploaded file based on metadata.

        Returns:
            str: The computed path of the uploaded file.
        """
        # Implement the method to compute the path of the uploaded file based on metadata
        # Example: return os.path.join('uploads', self.uid)
        return ''


if __name__ == "__main__":
    # Create the Database Tables
    db_path = os.path.join('db', 'mydatabase.db')
    engine = create_engine(f'sqlite:///{db_path}')
    Base.metadata.create_all(engine)
