from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Order(Base):
    __tablename__ = 'orders'

    order_id = Column(Integer, primary_key=True)
    customer_id = Column(String, ForeignKey('customers.customer_id'))
    employee_id = Column(Integer, ForeignKey('employees.employee_id'))
    order_date = Column(DateTime)
    required_date = Column(DateTime)
    shipped_date = Column(DateTime)
    ship_via = Column(Integer, ForeignKey('shippers.shipper_id'))
    freight = Column(Numeric)
    ship_name = Column(String)
    ship_address = Column(String)
    ship_city = Column(String)
    ship_region = Column(String)
    ship_postal_code = Column(String)
    ship_country = Column(String)

    # İlişkiler
    customer = relationship("Customer", back_populates="orders")
    order_details = relationship("OrderDetail", back_populates="order")