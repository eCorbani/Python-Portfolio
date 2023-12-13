"""
    Docstring
"""
import pprint

import sqlalchemy
from sqlalchemy import (Column,
                        String,
                        Integer,
                        ForeignKey,
                        Float,
                        create_engine,
                        inspect,
                        select
                        )

from sqlalchemy.orm import (declarative_base,
                            relationship,
                            Session)

Base = declarative_base()


class Customer(Base):
    """
        Customer definition
    """

    __tablename__ = "customer"

    #   Attributes

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    register_number = Column(String(9), nullable=False)
    address = Column(String, nullable=False)

    # Relationship
    account = relationship("Account", back_populates="customer", cascade="all, delete-orphan")

    def __repr__(self):
        return (
            f"Customer (id = {self.id}, "
            f"name = {self.name}, "
            f"register_number = {self.register_number}, "
            f"address = {self.address})"
        )


class Account(Base):
    """
        Account definition
    """

    __tablename__ = "account"

    # Attributes

    id = Column(Integer, primary_key=True, autoincrement=True)
    account_type = Column(String, nullable=False)
    agency = Column(String, nullable=False)
    account_number = Column(Integer, nullable=False)
    customer_id = Column(Integer, ForeignKey("customer.id"), nullable=False)
    balance = Column(Float)

    def __repr__(self):
        return (
            f"Account (id = {self.id}, "
            f"account_type = {self.account_type}, "
            f"agency = {self.agency}, "
            f"account_number = {self.account_number})"
            f"balance = {self.balance})"
        )

    # Relationship
    customer = relationship("Customer", back_populates="account")


#  DB connection
engine = create_engine("sqlite://")

#  Creating class as tables in the DB
Base.metadata.create_all(engine)

#  Inspect DB schema
engine_inspector = inspect(engine)

with Session(engine) as sessions:
    edson = Customer(
        name="edson",
        register_number="07070707077",
        address="St, 156 - bla bla bla",
        account=[
            Account(
                account_type="Individual",
                agency="0001",
                account_number=1,
                balance=0.0
            ),
            Account(
                account_type="Individual",
                agency="0001",
                account_number=2,
                balance=100.00
            )

        ]
    )
    joao = Customer(
        name="joao",
        register_number="07070707055",
        address="St, 99 - bla bla bla",
        account=[
            Account(
                account_type="Individual",
                agency="0001",
                account_number=3,
                balance=0.0
            )
        ]
    )
    #  Sending to DB
    sessions.add_all([edson, joao])
    sessions.commit()

stmt_customer = select(Customer).where(Customer.name.in_(["edson", "joao"]))
print("\nReturn users by a filter condition.")
for customer in sessions.scalars(stmt_customer):
    pprint.pprint(customer)

stmt_account = select(Account).where(Account.customer_id.isnot(None))
print("\nReturn Accounts.")
for account in sessions.scalars(stmt_account):
    pprint.pprint(account)
