from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from create_table import connect_db
import sqlite3
import random
from validate import validate_txn
from consume import consume_update
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Function to check if a user exists in the database
def user_exists(username):
    conn = sqlite3.connect("arqdb.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM user WHERE username=?", (username,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    connect_db()
    return templates.TemplateResponse("landing.html", {"request": request})

@app.get("/login" , response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/signup" , response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/user-signup", response_class=HTMLResponse)
async def signup(request: Request,username: str = Form(...), password: str = Form(...)):
    if user_exists(username):
        raise HTTPException(status_code=400, detail="User already exists")
    
    # Here, you should add logic to securely hash and store the password.
    # For simplicity, we'll store it as plaintext.
    
    conn = sqlite3.connect("arqdb.db")
    cursor = conn.cursor()
    coinvalue  = random.randint(1, 10)
    cursor.execute("INSERT INTO user (username, password, coinvalue) VALUES (?, ?, ?)", (username, password, coinvalue))
    result = {
        "id": cursor.lastrowid,
        "username": username,
        "password": password,
        "wallet" : 200,
        "coinvalue": coinvalue
    }
    conn.commit()
    conn.close()
    
    return templates.TemplateResponse("home.html" , {"user_data" : result, "request": request})

@app.post("/user-login", response_class=HTMLResponse)
def login(request: Request,username: str = Form(...), password: str = Form(...)):
    
    if not user_exists(username):
        raise HTTPException(status_code=400, detail="User not found")
    
    # Here, you should add logic to check the password securely.
    # For simplicity, we'll compare it as plaintext.
    
    conn = sqlite3.connect("arqdb.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE username=? AND password=?", (username, password))
    result = cursor.fetchone()
    if result:
        column_names = [description[0] for description in cursor.description]
        result = dict(zip(column_names, result))
    conn.close()

    if result is not None:
        return templates.TemplateResponse("home.html" , {"user_data" : result, "request": request})
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/send_amount", response_class=HTMLResponse)
async def send_amount(request: Request, sender_username: str = Form(...), transaction_amount: float = Form(...) , recipient_username: str = Form(...) ):
    print(sender_username)
    print(transaction_amount)
    print(recipient_username)
    try:
        validate_txn(username=sender_username, receiver_un=recipient_username, txn_amount=transaction_amount)
        return templates.TemplateResponse("txn_success.html", {"request": request})
    except Exception as e:

        return templates.TemplateResponse("txn_failed.html", {"request": request})

@app.post("/get_data")
def get_data():
    #data = consume_update('ashutosh')
    data = {"message": "Wallet balance"}
    print(data)
    return data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)





