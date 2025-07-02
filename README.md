# 📘 AnchorScore API Documentation

**Version:** 0.1.0

Score and assess risk levels for companies using AI systems.


## `POST /score` — Score company AI risk

Calculates a basic AI risk score based on usage level and revenue.

### 🔑 Parameters:
- **x-api-key** (header, `string`)

### ✅ Responses:
- **200**: Successful Response
- **422**: Validation Error

## `POST /upload` — Upload File

### 🔑 Parameters:
- **x-api-key** (header, `string`)

### ✅ Responses:
- **200**: Successful Response
- **422**: Validation Error

## `POST /data` — Ingest Data

### 🔑 Parameters:
- **x-api-key** (header, `string`)

### ✅ Responses:
- **200**: Successful Response
- **422**: Validation Error

## `GET /` — Health check

### ✅ Responses:
- **200**: Successful Response