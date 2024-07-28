from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database setup
DATABASE_URL = 'sqlite:///market_data.db'
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Define OHLCV model
class OHLCV(Base):
    __tablename__ = 'ohlcv_data'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)  # Changed from 'timestamp' to 'date'
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)
    average = Column(Float)  # New column
    barCount = Column(Integer)  # New column
    symbol = Column(String)

# Create tables
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
