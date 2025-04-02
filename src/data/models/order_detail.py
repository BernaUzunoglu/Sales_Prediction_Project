from sqlalchemy import Column, Integer, SmallInteger, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import REAL
from ..database import Base

class OrderDetail(Base):
    __tablename__ = 'order_details'

    order_id = Column(Integer, ForeignKey('orders.order_id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('products.product_id'), primary_key=True)
    unit_price = Column(Numeric)
    quantity = Column(SmallInteger)
    discount = Column(REAL)

    # İlişkiler
    order = relationship("Order", back_populates="order_details")
    product = relationship("Product", back_populates="order_details")