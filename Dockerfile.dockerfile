FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Environment
ENV FLASK_ENV=production \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    SECRET_KEY=change-me

EXPOSE 5000

# Single worker keeps SQLite happy
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:5000", "app:app"]