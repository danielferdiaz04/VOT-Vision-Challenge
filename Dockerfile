FROM python:3.9-slim

SHELL ["/bin/bash", "-c"] 

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \	
    nano \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1 \ 
    wget \
    unzip \
    && apt-get clean

# Crear directorio de trabajo
WORKDIR "/home/vot-workspace"

# Instalar dependencias Python
RUN pip install --upgrade pip && \
    pip install numpy opencv-python vot-toolkit==0.5.3 vot-trax==3.0.2

# Instalar VOT Trax 3.0.2 desde GitHub
#RUN git clone --branch v3.0.2 https://github.com/votchallenge/trax.git /opt/trax && \
#    cd /opt/trax && \
#    pip install .

# Definir punto de entrada (opcional)
CMD ["python3"]

