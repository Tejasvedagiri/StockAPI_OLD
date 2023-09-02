import uuid
from sqlalchemy import Column, String, Date, DECIMAL
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class StockTransaction(Base):
    __tablename__ = 'StockTransaction'
    ID = Column(CHAR(36), primary_key=True, default=str(uuid.uuid4()), unique=True, index=True)
    UserID = Column(CHAR(36), index=True)
    ActiveDate = Column(Date)
    ProcessDate = Column(Date)
    Instrument = Column(String, index=True)
    Description = Column(String)
    TransCode = Column(String)
    Quantity = Column(DECIMAL(precision=30, scale=30))
    Price = Column(DECIMAL(precision=30, scale=30))  # Decimal data type with precision and scale
    Amount = Column(DECIMAL(precision=30, scale=30)) 