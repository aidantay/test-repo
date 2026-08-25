FROM python:3.13-slim

WORKDIR /app

# Install procps (required by Nextflow)
RUN apt-get update && \
    apt-get install -y --no-install-recommends procps && \
    rm -rf /var/lib/apt/lists/*

# Copy common library and stage directory
COPY commons/ ./commons/
COPY stages/01-windows/ ./stages/01-windows/

# Install dependencies using standard pip directly into system python and clean up caches
RUN pip install --no-cache-dir ./commons/shared_libs && \
    pip install --no-cache-dir ./stages/01-windows && \
    find /usr/local -depth -name '__pycache__' -exec rm -rf {} \;

# Start bash by default
CMD ["/bin/bash"]
