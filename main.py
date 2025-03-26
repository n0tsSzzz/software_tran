from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from models import *

def _setup_database(engine):
    Base.metadata.create_all(engine)

def _get_session():
    db_user = os.getenv('PG_USER', 'postgres')
    db_pass = os.getenv('PG_PASS', 'postgres')
    db_host = os.getenv('PG_HOST', 'db')
    db_port = os.getenv('PG_PORT', '5432')
    db_name = os.getenv('PG_DATABASE', 'mydb')

    db_url = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    engine = create_engine(db_url)
    _setup_database(engine)
    return sessionmaker(bind=engine)()

def create_test_customer(session):
    try:
        customer = session.get(Customer, 1)
        if not customer:
            new_customer = Customer(
                first_name="John",
                last_name="Doe",
                email="john.doe@example.com"
            )
            session.add(new_customer)
            session.commit()
            print("Created test customer with ID: 1")
    except Exception as e:
        session.rollback()
        raise e


def place_order(db_session_, customer_id, items):
    try:
        with db_session_.begin():
            new_order = Order(
                customer_id=customer_id,
                order_date=date.today(),
                total_amount=0
            )
            db_session_.add(new_order)
            db_session_.flush()

            total = 0
            for product_id_, quantity in items:
                product = db_session.get(Product, product_id_)
                if not product:
                    raise ValueError(f"Product {product_id_} not found")

                subtotal = product.price * quantity
                item = OrderItem(
                    order_id=new_order.order_id,
                    product_id=product_id_,
                    quantity=quantity,
                    subtotal=subtotal
                )
                db_session_.add(item)
                total += subtotal

            new_order.total_amount = total
        return new_order.order_id
    except Exception as e_:
        db_session_.rollback()
        raise e_


def update_email(db_session_, customer_id, new_email):
    try:
        with db_session_.begin():
            customer = db_session_.get(Customer, customer_id)
            if not customer:
                raise ValueError("Customer not found")
            customer.email = new_email
    except Exception as e_:
        db_session.rollback()
        raise e_


def add_product(db_session_, product_name, price):
    try:
        with db_session_.begin():
            product = Product(
                product_name=product_name,
                price=price
            )
            db_session_.add(product)
            db_session_.flush()
            return product.product_id
    except Exception as e_:
        db_session_.rollback()
        raise e_


if __name__ == '__main__':
    with _get_session() as db_session:
        try:
            create_test_customer(db_session)

            product_id = add_product(db_session, "Super Product", 49.99)
            print(f"Added product ID: {product_id}")

            update_email(db_session, 1, "new.email@example.com")
            print("Email updated")

            order_id = place_order(db_session, 1, [(product_id, 2)])
            print(f"Created order ID: {order_id}")

        except Exception as e:
            print(f"Error: {e}")
            db_session.rollback()