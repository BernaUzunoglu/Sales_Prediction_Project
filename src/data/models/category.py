from sqlalchemy import Column, String, Integer, LargeBinary
from sqlalchemy.orm import relationship
from ..database import Base
class Category(Base):
    __tablename__ = 'categories'

    category_id = Column(Integer, primary_key=True)
    category_name = Column(String)
    description = Column(String)
    picture = Column(LargeBinary)

    # İlişkiler
    products = relationship("Product", back_populates="category")