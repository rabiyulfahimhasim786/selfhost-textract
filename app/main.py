from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.responses import JSONResponse
from app.extract import process_file
import os

app = FastAPI(title="Selfhost Textract GST API")

@app.post('/extract')
async def extract(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    contents = await file.read()
    dest = os.path.join('/tmp', file.filename)
    with open(dest, 'wb') as f:
        f.write(contents)

    # run processing in background and return a job id-like stub
    if background_tasks is not None:
        background_tasks.add_task(process_file, dest)
        return JSONResponse({'status': 'processing', 'file': file.filename})

    # synchronous fallback
    result = process_file(dest)
    return JSONResponse(result)

@app.get('/')
def root():
    return {"message": "Selfhost Textract GST API — upload PDF/image to /extract"}