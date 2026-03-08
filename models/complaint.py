from sqlalchemy import Column, BigInteger, String, DateTime, Float, Text
from datetime import datetime, timezone
from models.user import Base 



class Complaint(Base):
    __tablename__ = "nyc_311_service_requests"

    unique_key                     = Column(BigInteger, primary_key=True)
    created_date                   = Column(DateTime, nullable=False)
    closed_date                    = Column(DateTime, nullable=True)
    agency                         = Column(String, nullable=False)
    agency_name                    = Column(String, nullable=False)
    complaint_type                 = Column(String, nullable=False)
    descriptor                     = Column(String, nullable=True)
    location_type                  = Column(String, nullable=True)
    incident_zip                   = Column(String, nullable=True)
    city                           = Column(String, nullable=True)
    borough                        = Column(String, nullable=False)
    status                         = Column(String, nullable=False)
    resolution_description         = Column(Text,   nullable=True)
    latitude                       = Column(Float,  nullable=True)
    longitude                      = Column(Float,  nullable=True)
    resolution_action_updated_date = Column(DateTime, nullable=True)