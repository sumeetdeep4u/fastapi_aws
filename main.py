from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from models import User
from crud import get_users, create_user, get_user, delete_user, upload_file_to_s3

app = FastAPI()

@app.get("/")
def list_users(limit: int = 20):
    return get_users(limit)

@app.post("/users/")
async def add_user(
    user_id: str = Form(...),
    name: str = Form(...),
    email: str = Form(...),
    file: UploadFile = File(...)
):
    file_url = upload_file_to_s3(file, file.filename)
    user_data = {
        "user_id": user_id,
        "name": name,
        "email": email,
        "file_url": file_url
    }
    return create_user(user_data)

@app.get("/users/{user_id}")
def read_user(user_id: str):
    user = get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.delete("/users/{user_id}")
def remove_user(user_id: str):
    delete_user(user_id)
    return {"message": f"User {user_id} deleted successfully"}
