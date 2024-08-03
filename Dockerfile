FROM ghcr.io/osgeo/gdal:ubuntu-small-3.5.0 as base

RUN apt-get update && apt-get install -y \
    git \
    python3-pip \
    python3.8 \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install --upgrade \
    pip \
    setuptools \
    wheel

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install \
  django-large-image \
  'large-image[rasterio,pil]>=1.22'
RUN pip install numpy>1.0.0 wheel setuptools>=67
RUN pip install --no-cache-dir --force-reinstall gdal==3.5.0

# Copy over the entire project
COPY . .

# Give permission
RUN chmod +x /app/entrypoint.sh

# Set working directory for Django app
WORKDIR /app

# Run the entrypoint script
CMD ["./entrypoint.sh"]
