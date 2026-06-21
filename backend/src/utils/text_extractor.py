from fastapi import HTTPException, UploadFile


async def extract_text(file: UploadFile) -> str:
    if file.content_type == "text/plain":
        content = await file.read()
        return content.decode("utf-8")

    raise HTTPException(status_code=400, detail="Unsupported file type")
