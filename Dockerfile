 FROM python:3.11-slim
 ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
 WORKDIR /app
 # system deps for pdf2image, opencv, camelot, poppler
 RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential poppler-utils libgl1 libglib2.0-0 git curl wget pkg-config \
    libcairo2-dev libjpeg-dev libpoppler-cpp-dev python3-dev \
 && rm -rf /var/lib/apt/lists/*
 COPY requirements.txt .
 RUN pip install --upgrade pip
 RUN ls
 RUN pip install --no-cache-dir -r requirements.txt
 RUN pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
 RUN pip install 'layoutparser[detectron2]==0.3.4'
 COPY . /app
 EXPOSE 8000
 CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]