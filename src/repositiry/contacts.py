from sqlalchemy.orm import Session
from sqlalchemy import and_, func

from src.database.models import Contact
from src.schemas import ContactModel


async def get_contacts(limit: int, offset: int, db: Session):
    contacts = db.query(Contact).limit(limit).offset(offset).all()
    return contacts


async def get_contact_by_id(contact_id: int, db: Session):
    contact = db.query(Contact).filter_by(id=contact_id).first()
    return contact


async def get_contact_by_name(name: str, db: Session):
    contacts = db.query(Contact).filter_by(name=name).all()
    return contacts


async def get_contact_by_surname(surname: str, db: Session):
    contacts = db.query(Contact).filter_by(surname=surname).all()
    return contacts


async def get_contact_by_email(email: str, db: Session):
    contact = db.query(Contact).filter_by(email=email).first()
    return contact


async def get_nearly_birthdays(db: Session):
    contact = db.query(Contact) \
        .select_from(Contact) \
        .filter(and_(func.date_part('day', Contact.birthday) - func.date_part('day', func.current_date()) <= 7,
                     func.date_part('month', Contact.birthday) == func.date_part('month', func.current_date()))) \
        .all()
    return contact


async def create(body: ContactModel, db: Session):
    contact = Contact(name=body.name, surname=body.surname, phone=body.phone, \
                      email=body.email, birthday=body.birthday, description=body.description)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update(contact_id: int, body: ContactModel, db: Session):
    contact = await get_contact_by_id(contact_id, db)
    if contact:
        contact.name = body.name
        contact.surname = body.surname
        contact.phone = body.phone
        contact.email = body.email
        contact.surname = body.surname
        contact.birthday = body.birthday
        contact.description = body.description
        db.commit()
    return contact


async def remove(contact_id: int, db: Session):
    contact = await get_contact_by_id(contact_id, db)
    if contact:
        db.delete(contact)
        db.commit()
    return contact
