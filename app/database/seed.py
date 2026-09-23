from datetime import datetime, timedelta
import random

from faker import Faker

from app.database.session import SessionLocal
from app.models.customer import Customer
from app.models.product import Product
from app.models.order import Order
from app.models.order_item import OrderItem

fake = Faker()
db = SessionLocal()


## generate customers
customers = []

for _ in range(50):
    customer = Customer(
        name=fake.name(),
        email=fake.unique.email()
    )

    db.add(customer)
    customers.append(customer)

db.commit()


## generate products
products = []

for _ in range(100):
    product = Product(
        name=fake.word().capitalize(),
        price=round(random.uniform(100,50000),2)
    )

    db.add(product)
    products.append(product)

db.commit()


## generate orders
orders = []

for _ in range(500):

    customer = random.choice(customers)

    order = Order(
        customer_id=customer.id,
        order_date=fake.date_time_between(
            start_date="-1y",
            end_date="now"
        ),
        total_amount=0
    )

    db.add(order)
    orders.append(order)

db.commit()

## generate order items
for order in orders:

    total = 0

    chosen = random.sample(
        products,
        random.randint(1,5)
    )

    for product in chosen:

        qty = random.randint(1,3)

        item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=qty
        )

        db.add(item)

        total += float(product.price)*qty

    order.total_amount = round(total,2)

db.commit()

db.close()