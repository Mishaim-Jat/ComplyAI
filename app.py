import os
import shutil
from fastapi import FastAPI, UploadFile, File, Request, Form, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jose import jwt
from datetime import datetime, timezone

from database import SessionLocal, User, Document
from auth_utils import hash_password, verify_password, create_token, SECRET_KEY, ALGORITHM
import compliance

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("session")
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        return db.query(User).filter(User.email == email).first()
    except:
        return None

# --- ROUTES ---
@app.get("/")
async def home(request: Request, user=Depends(get_current_user)):
    return templates.TemplateResponse("index.html", {"request": request, "user": user})

@app.get("/signup")
async def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/signup")
async def signup_action(
    request: Request,
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    db: Session = Depends(get_db),
):
    if password != confirm_password:
        return templates.TemplateResponse(
            "signup.html", {"request": request, "error": "Passwords do not match"}
        )

    existing = db.query(User).filter(User.email == email).first()
    if existing:
        return templates.TemplateResponse(
            "signup.html", {"request": request, "error": "Email already registered"}
        )

    new_user = User(
        email=email,
        hashed_password=hash_password(password),
        first_name=first_name,
        last_name=last_name,
    )
    db.add(new_user)
    db.commit()
    return RedirectResponse(
        url="/login", status_code=status.HTTP_303_SEE_OTHER
    )

@app.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login_action(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return templates.TemplateResponse(
            "login.html", {"request": request, "error": "Invalid credentials"}
        )

    token = create_token(data={"sub": user.email})
    response = RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="session", value=token, httponly=True)
    return response

@app.get("/dashboard")
async def dashboard(
    request: Request, user=Depends(get_current_user), db: Session = Depends(get_db)
):
    if not user:
        return RedirectResponse(url="/login")

    docs = db.query(Document).all()
    stats = {
        "all": len(docs),
        "compliant": len([d for d in docs if d.status == "Compliant"]),
        "review": len([d for d in docs if d.status == "Under Review"]),
    }

    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "user": user, "documents": docs, "stats": stats},
    )

@app.get("/upload")
async def upload_page(request: Request, user=Depends(get_current_user)):
    if not user:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("upload.html", {"request": request, "user": user})

@app.post("/upload")
async def upload(
    request: Request,
    policy_file: UploadFile = File(...),
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not user:
        return RedirectResponse(url="/login")

    policy_path = os.path.join(UPLOAD_DIR, policy_file.filename)
    with open(policy_path, "wb") as f:
        shutil.copyfileobj(policy_file.file, f)

    results = compliance.analyze(policy_path)

    new_doc = Document(
        file_name=policy_file.filename,
        status="Under Review",
        compliance_score=75.0,
    )
    db.add(new_doc)
    db.commit()

    return templates.TemplateResponse(
        "results.html",
        {
            "request": request,
            "user": user,
            "file_name": policy_file.filename,
            "results": results,
        },
    )

@app.get("/calendar")
async def calendar_page(request: Request, user=Depends(get_current_user)):
    if not user:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("calander.html", {"request": request, "user": user})

@app.get("/api/calendar-events")
async def get_calendar_events(user=Depends(get_current_user), db: Session = Depends(get_db)):
    if not user:
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    
    docs = db.query(Document).all()
    events = []
    for doc in docs:
        if doc.status == "Compliant":
            className = "compliant"
        elif doc.status == "Overdue":
            className = "overdue"
        else:
            className = "under-review"
        
        events.append({
            "title": doc.file_name,
            "start": datetime.now().strftime("%Y-%m-%d"),
            "className": className,
            "extendedProps": {
                "status": doc.status,
                "owner": f"User",
                "notes": f"Score: {doc.compliance_score}%",
            }
        })
    
    return JSONResponse(events)

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/")
    response.delete_cookie("session")
    return response

# --- FORGOT PASSWORD ---
def send_reset_email(email: str, reset_token: str):
    smtp_email = os.getenv("SMTP_EMAIL")
    smtp_password = os.getenv("SMTP_PASSWORD")
    
    reset_link = f"http://localhost:8000/reset-password?token={reset_token}"
    
    message = MIMEMultipart()
    message["From"] = smtp_email
    message["To"] = email
    message["Subject"] = "Password Reset"
    
    body = f"Click to reset: {reset_link}"
    message.attach(MIMEText(body, "html"))
    
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(smtp_email, smtp_password)
        server.send_message(message)

@app.get("/forgot-password")
async def forgot_password_page(request: Request):
    return templates.TemplateResponse("forgot_password.html", {"request": request})

@app.post("/forgot-password")
async def forgot_password_action(
    request: Request,
    email: str = Form(...),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == email).first()
    
    if not user:
        return templates.TemplateResponse(
            "forgot_password.html", 
            {"request": request, "error": "Email not found"}
        )
    
    from auth_utils import generate_reset_token, token_expiry_time
    reset_token = generate_reset_token()
    reset_expiry = token_expiry_time()
    
    user.reset_token = reset_token
    user.reset_token_expiry = reset_expiry
    db.commit()
    
    try:
        send_reset_email(user.email, reset_token)
        return templates.TemplateResponse(
            "forgot_password.html",
            {"request": request, "message": "Reset link sent"}
        )
    except:
        return templates.TemplateResponse(
            "forgot_password.html",
            {"request": request, "error": "Failed to send email"}
        )

@app.get("/reset-password")
async def reset_password_page(request: Request, token: str = None):
    return templates.TemplateResponse(
        "reset_password.html", 
        {"request": request, "token": token}
    )

@app.post("/reset-password")
async def reset_password_action(
    request: Request,
    token: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    db: Session = Depends(get_db),
):
    if password != confirm_password:
        return templates.TemplateResponse(
            "reset_password.html",
            {"request": request, "error": "Passwords do not match", "token": token}
        )
    
    user = db.query(User).filter(User.reset_token == token).first()
    
    if not user:
        return templates.TemplateResponse(
            "reset_password.html",
            {"request": request, "error": "Invalid token"}
        )
    
    if user.reset_token_expiry < datetime.now():
        return templates.TemplateResponse(
            "reset_password.html",
            {"request": request, "error": "Token expired"}
        )
    
    user.hashed_password = hash_password(password)
    user.reset_token = None
    user.reset_token_expiry = None
    db.commit()
    
    return templates.TemplateResponse(
        "reset_password.html",
        {"request": request, "message": "Password reset successfully!"}
    )

@app.get("/api/calendar-events")
async def get_calendar_events(user=Depends(get_current_user), db: Session = Depends(get_db)):
    if not user:
        return JSONResponse({"error": "Unauthorized"}, status_code=401)
    
    docs = db.query(Document).all()
    events = []
    for doc in docs:
        if doc.status == "Compliant":
            className = "compliant"
        elif doc.status == "Overdue":
            className = "overdue"
        else:
            className = "under-review"
        
        # Use created_at date if available, otherwise use today
        if hasattr(doc, 'created_at') and doc.created_at:
            event_date = doc.created_at.strftime("%Y-%m-%d")
        else:
            event_date = datetime.now().strftime("%Y-%m-%d")
        
        events.append({
            "title": doc.file_name,
            "start": event_date,
            "className": className,
            "extendedProps": {
                "status": doc.status,
                "owner": f"User",
                "notes": f"Score: {doc.compliance_score}%",
            }
        })
    
    return JSONResponse(events)