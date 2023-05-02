FROM python:3.9
COPY ./requirements.txt /requirements.txt
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install -r /requirements.txt
RUN pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu
COPY . /app/
CMD ["python", "app/main.py"]