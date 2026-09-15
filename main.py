from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, Base, get_db
import models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Wholesale Billing Engine")

@app.get("/")
def home():
    return {"message": "Wholesale Billing & Inventory System Live!"}

@app.post("/stock/add")
def add_set_stock(item_code: str, name: str, category: str, set_details: str, fix_price: float, sets_qty: int, db: Session = Depends(get_db)):
    product = models.Product(
        item_code=item_code,
        item_name=name,
        category=category,
        set_details=set_details,
        fix_price_per_set=fix_price,
        available_sets=sets_qty
    )
    db.add(product)
    db.commit()
    return {"status": "Success", "message": f"{sets_qty} sets added for {name}"}

@app.post("/order/create")
def create_wholesale_order(
    customer_phone: str,
    customer_name: str,
    item_code: str,
    sets_ordered: int,
    cash_paid: float,
    online_paid: float,
    db: Session = Depends(get_db)
):
    product = db.query(models.Product).filter(models.Product.item_code == item_code).first()
    if not product:
        raise HTTPException(status_code=404, detail="Item code not found!")
    if product.available_sets < sets_ordered:
        raise HTTPException(status_code=400, detail=f"Only {product.available_sets} sets available!")

    total_bill = product.fix_price_per_set * sets_ordered
    total_received = cash_paid + online_paid
    due = total_bill - total_received

    customer = db.query(models.Customer).filter(models.Customer.phone == customer_phone).first()
    if not customer:
        customer = models.Customer(name=customer_name, phone=customer_phone, balance_due=0.0)
        db.add(customer)
        db.commit()
        db.refresh(customer)

    if due > 0:
        customer.balance_due += due

    product.available_sets -= sets_ordered

    order = models.Order(
        customer_id=customer.id,
        total_amount=total_bill,
        cash_paid=cash_paid,
        online_paid=online_paid,
        due_amount=due
    )
    db.add(order)
    db.commit()

    return {
        "status": "Order Success",
        "customer": customer.name,
        "item": product.item_name,
        "sets_purchased": sets_ordered,
        "total_bill": total_bill,
        "paid_cash": cash_paid,
        "paid_online": online_paid,
        "remaining_udhari_added": due,
        "stock_left": product.available_sets
    }