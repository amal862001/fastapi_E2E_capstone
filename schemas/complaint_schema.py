from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# The data user receives when getting a complaint.

class ComplaintResponse(BaseModel):
    unique_key              : int
    created_date            : datetime
    closed_date             : Optional[datetime]
    agency                  : str
    agency_name             : str
    complaint_type          : str
    descriptor              : Optional[str]
    location_type           : Optional[str]
    incident_zip            : Optional[str]
    city                    : Optional[str]
    borough                 : str
    status                  : str
    resolution_description  : Optional[str]
    latitude                : Optional[float]
    longitude               : Optional[float]
    resolution_action_updated_date : Optional[datetime]

    class Config:
        from_attributes = True


# The data user sends when creating a new complaint.

class ComplaintCreate(BaseModel):
    complaint_type  : str
    descriptor      : Optional[str]
    incident_zip    : Optional[str]
    city            : Optional[str]
    borough         : str
    location_type   : Optional[str]
    latitude        : Optional[float]
    longitude       : Optional[float]


# The data user sends when updating a complaint. 

class ComplaintUpdate(BaseModel):
    status                  : Optional[str]
    resolution_description  : Optional[str]    