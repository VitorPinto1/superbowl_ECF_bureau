# Dockerfile

FROM python:3.9

# Installer ce qu'il faut pour le GUI Tkinter
RUN apt-get update && apt-get install -y \
    python3-tk \
    libx11-6 \
    libgl1-mesa-glx \
    x11-apps \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

ENV DISPLAY=:0

CMD ["python", "main.py"]
