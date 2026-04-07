FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu20.04
RUN apt-get update && apt-get install -y python3 python3-pip poppler-utils libgl1-mesa-glx
RUN pip3 install runpod paddlepaddle-gpu paddleocr pdf2image Pillow numpy
COPY handler.py .
CMD ["python3", "-u", "handler.py"]
