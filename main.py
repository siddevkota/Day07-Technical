from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import mysql.connector
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="User Logs API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "user_logs_db"),
        port=int(os.getenv("DB_PORT", "3306")),
    )


class UserLog(BaseModel):
    user_id: int
    action: str
    message: Optional[str] = None


@app.post("/log")
async def create_log(log: UserLog, request: Request):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO user_action_logs (user_id, action, message, ip_address, user_agent) VALUES (%s, %s, %s, %s, %s)",
            (
                log.user_id,
                log.action,
                log.message,
                request.client.host if request.client else "unknown",
                request.headers.get("user-agent"),
            ),
        )
        db.commit()
        return {"status": "success", "id": cursor.lastrowid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        if "db" in locals():
            db.close()


@app.get("/logs/{user_id}")
async def get_user_logs(user_id: int):
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM user_action_logs WHERE user_id = %s ORDER BY created_at DESC",
            (user_id,),
        )
        return cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        if "db" in locals():
            db.close()


@app.get("/logs")
async def get_all_logs():
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM user_action_logs ORDER BY created_at DESC LIMIT 100"
        )
        return cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        if "db" in locals():
            db.close()


@app.get("/", response_class=HTMLResponse)
async def serve_interface():
    with open("log_interface.html", "r", encoding="utf-8") as file:
        return file.read()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
