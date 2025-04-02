from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from ..database import Base
class Customer(Base):
    __tablename__ = 'customers'

    customer_id = Column(String, primary_key=True)
    company_name = Column(String)
    contact_name = Column(String)
    contact_title = Column(String)
    address = Column(String)
    city = Column(String)
    region = Column(String)
    postal_code = Column(String)
    country = Column(String)
    phone = Column(String)
    fax = Column(String)

    # İlişkiler
    orders = relationship("Order", back_populates="customer")