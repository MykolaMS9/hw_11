from typing import List

from fastapi import Depends, HTTPException, status, Path, APIRouter, Query
from sqlalchemy.orm import Session

from src.repositiry import contacts as repository_contacts
from src.database.db import get_db
from src.schemas import ContactResponse, ContactModel

router = APIRouter(prefix='/contact', tags=['contact'])


@router.get("/", response_model=List[ContactResponse])
async def get_contacts(limit: int = Query(10, le=500), offset: int = 0, db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_contacts(limit, offset, db)
    return contacts


# response_model=OwnerResponse,
@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_contact_by_id(contact_id, db)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contacts


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactModel, db: Session = Depends(get_db)):
    contact = await repository_contacts.create(body, db)
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(body: ContactModel, contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = await repository_contacts.update(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contact


@router.patch("/{contact}/name", response_model=List[ContactResponse])
async def get_contact_by_name(contact_name: str, db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_contact_by_name(contact_name, db)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contacts


@router.patch("/{contact}/surname", response_model=List[ContactResponse])
async def get_contact_by_surname(contact_surname: str, db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_contact_by_surname(contact_surname, db)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contacts


@router.patch("/{contact}/email", response_model=ContactResponse)
async def get_contact_by_email(contact_email: str, db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact_by_email(contact_email, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contact


@router.patch("/{contact}/birthdays", response_model=List[ContactResponse])
async def get_contacts_nearly_birthdays(db: Session = Depends(get_db)):
    contact = await repository_contacts.get_nearly_birthdays(db)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = await repository_contacts.remove(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contact
