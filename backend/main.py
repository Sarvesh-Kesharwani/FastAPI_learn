from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException
from starlette import status

from sqlalchemy.orm import Session
from database import engine, SessionLocal

from typing import Annotated

# custom modules
import models
import auth

# backend.py
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import shutil
import os


from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import init_db, SessionLocal_summary
from llm_chain import summarize_doc
from datetime import datetime
from models import Summary


app = FastAPI()
app.include_router(auth.router)

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependecy = Annotated[Session, Depends(get_db)]


@app.get("/", status_code=status.HTTP_200_OK)
async def user(user: None, db: db_dependecy):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    return {"User": user}


UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

#####################################################################################################################################
# CORS for frontend access
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

init_db()


@app.post("/summarize")
async def summarize(user_id: str = Form(...), file: UploadFile = Form(...)):
    content = await file.read()
    summary_text = summarize_doc(content)

    db: Session = SessionLocal_summary()
    new_summary = Summary(
        user_id=user_id,
        file_name=file.filename,
        summary=summary_text,
        timestamp=datetime.now(),
    )
    db.add(new_summary)
    db.commit()
    db.refresh(new_summary)
    db.close()

    return {"summary": summary_text}


@app.get("/summaries")
def get_summaries(user_id: str):
    db: Session = SessionLocal_summary()
    results = (
        db.query(Summary)
        .filter(Summary.user_id == user_id)
        .order_by(Summary.timestamp.desc())
        .all()
    )
    db.close()
    return [
        {
            "file_name": r.file_name,
            "summary": r.summary,
            "timestamp": r.timestamp.isoformat(),
        }
        for r in results
    ]
