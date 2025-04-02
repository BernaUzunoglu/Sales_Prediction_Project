from sqlalchemy import Column, Integer, String, SmallInteger, Numeric, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from ..database import Base

class Product(Base):
    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True)
    product_name = Column(String)
    supplier_id = Column(Integer, ForeignKey('suppliers.supplier_id'))
    category_id = Column(Integer, ForeignKey('categories.category_id'))
    quantity_per_unit = Column(String)
    unit_price = Column(Numeric)
    units_in_stock = Column(SmallInteger)
    units_on_order = Column(SmallInteger)
    reorder_level = Column(SmallInteger)
    discontinued = Column(Boolean)

    # Bunları sonra tanımlayabilirsin, önce model çalışsın:
    category = relationship("Category", back_populates="products")
    order_details = relationship("OrderDetail", back_populates="product")
