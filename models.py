from datetime import date
from decimal import Decimal
from sqlalchemy import ForeignKey, Numeric, String, func
from sqlalchemy.schema import MetaData
from sqlalchemy.orm import Mapped, relationship, DeclarativeBase, mapped_column

# Recommended naming convention used by Alembic, as various different database
# providers will autogenerate vastly different names making migrations more
# difficult. See: https://alembic.sqlalchemy.org/en/latest/naming.html
NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


DEFAULT_SCHEMA = "public"

metadata = MetaData(naming_convention=NAMING_CONVENTION, schema=DEFAULT_SCHEMA)

# ORM - objecct related model : python <-> databse


class Base(DeclarativeBase):
    metadata = metadata
    __table_args__ = {"schema": DEFAULT_SCHEMA}


class Customer(Base):
    __tablename__ = "customers"

    customer_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100))

    orders: Mapped[list["Order"]] = relationship(back_populates="customer")


class Product(Base):
    __tablename__ = "products"

    product_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_name: Mapped[str] = mapped_column(String(100))
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))

    order_items: Mapped[list["OrderItem"]] = relationship(back_populates="product")


class Order(Base):
    __tablename__ = "orders"

    order_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.customer_id", ondelete="CASCADE"))
    order_date: Mapped[date] = mapped_column(server_default=func.current_date())
    total_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))

    customer: Mapped["Customer"] = relationship(back_populates="orders")
    items: Mapped[list["OrderItem"]] = relationship(back_populates="order")


class OrderItem(Base):
    __tablename__ = "orderitems"

    order_item_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.order_id", ondelete="CASCADE"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.product_id", ondelete="CASCADE"))
    quantity: Mapped[int]
    subtotal: Mapped[Decimal] = mapped_column(Numeric(10, 2))

    order: Mapped["Order"] = relationship(back_populates="items")
    product: Mapped["Product"] = relationship(back_populates="order_items")