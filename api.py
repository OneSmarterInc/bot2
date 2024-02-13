

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import json

app = FastAPI()
origins = [
    "http://localhost:3000/",
    "http://localhost:8000/",
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directory to store uploaded PDF files
UPLOAD_DIR ="documents"


@app.post("/bot_api/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    # Create directory if it doesn't exist
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    # Check if the uploaded file is a PDF
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    # Save the uploaded file to the upload directory
    with open(os.path.join(UPLOAD_DIR, file.filename), "wb") as buffer:
        buffer.write(await file.read())

    return JSONResponse(content={"filename": file.filename, "message": "File uploaded successfully"})


@app.delete("/bot_api/delete/{filename}")
async def delete_pdf(filename: str):
    # Check if the file exists
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    # Delete the file
    os.remove(file_path)

    return JSONResponse(content={"filename": filename, "message": "File deleted successfully"})


@app.get("/bot_api/view/")
async def view_pdfs():
    # List all the PDF files in the upload directory
    pdf_files = []
    for file_name in os.listdir(UPLOAD_DIR):
        if file_name.endswith(".pdf"):
            pdf_files.append(file_name)

    return JSONResponse(content={"pdf_files": pdf_files})

predefined_key = "zioWntPw97"  # Change this to your actual key

# Path to store the usernames
usernames_file = "usernames.json"

@app.post("/bot_api/authenticate/")
async def authenticate(name: str, key: str):
    # Check if the key matches the predefined key
    print(name,key)
    if key != predefined_key:
        # If the key does not match, return an error
        raise HTTPException(status_code=401, detail="Authentication Failed")

    # Attempt to read the existing usernames
    try:
        with open(usernames_file, "r") as file:
            usernames = json.load(file)
    except FileNotFoundError:
        # If the file does not exist, start with an empty list
        usernames = []

    # Check if the username already exists
    if name in usernames:
        return {"message": "Welcome back!"}
    else:
        # If the username does not exist, add it to the list
        usernames.append(name)
        # Write the updated list back to the file
        with open(usernames_file, "w") as file:
            json.dump(usernames, file)
        return {"message": "Authenticated"}
