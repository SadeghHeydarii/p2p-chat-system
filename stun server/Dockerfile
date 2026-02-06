# =========================
# Base image
# =========================
FROM python:3.12

# =========================
# Environment variables
# =========================
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# =========================
# Working directory
# =========================
WORKDIR /app

# =========================
# Copy project files
# =========================
COPY . /app/

# =========================
# Install dependencies
# =========================
RUN pip install -i https://mirror-pypi.runflare.com/simple --no-cache-dir django

# =========================
# Expose Django port
# =========================
EXPOSE 8000

# =========================
# Run Django server
# =========================
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
