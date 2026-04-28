FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    gfortran \
    && rm -rf /var/lib/apt/lists/*

# Clone enumlib
RUN git clone --recursive https://github.com/msg-byu/enumlib.git

# Build enumlib
WORKDIR /app/enumlib/src
RUN make clean || true
RUN make FC=gfortran F90=gfortran CC=gcc

RUN make clean || true

# Build enum.x explicitly
RUN make enum.x FC=gfortran F90=gfortran CC=gcc

# Build makestr.x explicitly
RUN make makestr.x FC=gfortran F90=gfortran CC=gcc

# Make binaries accessible
ENV PATH="/app/enumlib/src:${PATH}"
RUN ln -s /app/enumlib/src/enum.x /usr/local/bin/enum.x && \
    ln -s /app/enumlib/src/makestr.x /usr/local/bin/makestr.x

# Back to app
WORKDIR /app

# Install Python deps
COPY ground_pymatgen/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your code
COPY ground_pymatgen/ .

CMD ["python", "generator.py"]
