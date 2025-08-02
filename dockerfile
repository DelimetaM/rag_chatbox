# Përdor imazhin zyrtar të Python
FROM python:3.11-slim

# Vendos direktorinë e punës
WORKDIR /app

# Kopjo të gjithë përmbajtjen e projektit në container
COPY . .

# Instalimi i varësive
RUN pip install --no-cache-dir -r requirements.txt

# Ekspozo portin për FastAPI
EXPOSE 8000

# Komanda për të startuar aplikacionin
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]