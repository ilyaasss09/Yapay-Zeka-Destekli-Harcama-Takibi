from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db, ExpenseDB
from ai_service import categorize_expense_with_ai

app = FastAPI(title="Yapay Zeka Destekli Harcama Takibi")

# Kullanıcıdan gelecek veri modeli (Pydantic ile doğrulama)
class ExpenseRequest(BaseModel):
    description: str
    amount: float

@app.get("/", response_class=HTMLResponse)
def read_root():
    """Basit bir arayüz sunar."""
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/add-expense/")
def add_expense(expense: ExpenseRequest, db: Session = Depends(get_db)):
    """Yeni harcama ekler ve yapay zeka ile kategorisini bulur."""
    
    # 1. Yapay Zeka Dil Modelinden kategoriyi al (AI Kriteri)
    predicted_category = categorize_expense_with_ai(expense.description)
    
    # 2. Veritabanına kaydet (Veritabanı Kriteri)
    new_expense = ExpenseDB(
        description=expense.description,
        amount=expense.amount,
        category=predicted_category
    )
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    
    return {"message": "Harcama başarıyla eklendi", "data": new_expense}

@app.get("/expenses/")
def get_expenses(db: Session = Depends(get_db)):
    """Tüm harcamaları listeler."""
    expenses = db.query(ExpenseDB).all()
    return expenses