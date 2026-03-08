from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from database import get_db
from dependencies import get_current_user
from models.user import PlatformUser
from models.complaint import Complaint
from schemas.complaint_schema import ComplaintResponse, ComplaintCreate, ComplaintUpdate

router = APIRouter(prefix="/complaints", tags=["Complaints"])


# Get all complaints (agency filtered)

@router.get("/", response_model=list[ComplaintResponse])
def get_complaints(
    borough     : Optional[str]      = Query(None),
    status      : Optional[str]      = Query(None),
    start_date  : Optional[datetime] = Query(None),
    end_date    : Optional[datetime] = Query(None),
    limit       : int                = Query(50, le=500),
    offset      : int                = Query(0),
    db          : Session            = Depends(get_db),
    current_user: PlatformUser       = Depends(get_current_user)
):
    query = db.query(Complaint).filter(
        Complaint.agency == current_user.agency_code
    )

    if borough:
        query = query.filter(Complaint.borough == borough.upper())

    if status:
        query = query.filter(Complaint.status == status)

    if start_date:
        query = query.filter(Complaint.created_date >= start_date)

    if end_date:
        query = query.filter(Complaint.created_date <= end_date)

    return query.offset(offset).limit(limit).all()


# Get single complaint

@router.get("/{unique_key}", response_model=ComplaintResponse)
def get_complaint(
    unique_key  : int,
    db          : Session      = Depends(get_db),
    current_user: PlatformUser = Depends(get_current_user)
):
    complaint = db.query(Complaint).filter(
        Complaint.unique_key == unique_key,
        Complaint.agency     == current_user.agency_code
    ).first()

    if complaint is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail      = "Complaint not found"
        )

    return complaint


# Create complaint

@router.post("/", response_model=ComplaintResponse, status_code=status.HTTP_201_CREATED)
def create_complaint(
    request     : ComplaintCreate,
    db          : Session      = Depends(get_db),
    current_user: PlatformUser = Depends(get_current_user)
):
    complaint = Complaint(
        complaint_type  = request.complaint_type,
        descriptor      = request.descriptor,
        incident_zip    = request.incident_zip,
        city            = request.city,
        borough         = request.borough.upper(),
        location_type   = request.location_type,
        latitude        = request.latitude,
        longitude       = request.longitude,
        agency          = current_user.agency_code,
        agency_name     = current_user.agency_code,
        status          = "Open",
        created_date    = datetime.utcnow()
    )

    db.add(complaint)
    db.commit()
    db.refresh(complaint)
    return complaint


# Update complaint

@router.patch("/{unique_key}", response_model=ComplaintResponse)
def update_complaint(
    unique_key  : int,
    request     : ComplaintUpdate,
    db          : Session      = Depends(get_db),
    current_user: PlatformUser = Depends(get_current_user)
):
    complaint = db.query(Complaint).filter(
        Complaint.unique_key == unique_key,
        Complaint.agency     == current_user.agency_code
    ).first()

    if complaint is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail      = "Complaint not found"
        )

    if request.status:
        complaint.status = request.status

    if request.resolution_description:
        complaint.resolution_description = request.resolution_description
        complaint.resolution_action_updated_date = datetime.utcnow()

    db.commit()
    db.refresh(complaint)
    return complaint