# EduDealsBot – Asistente de descuentos en cursos y certificaciones

Asistente que **recomienda cursos/certificaciones** con foco en **descuentos y convenios** asociados a **bancos chilenos** (Santander, Banco de Chile, BancoEstado).

## ¿Cómo funciona?
- Fuente de ofertas en `data/offers/*.json` (puedes actualizar manualmente o automatizar scraping/ingesta).
- Endpoint `/recommend` filtra por **banco**, **área** (ciberseguridad, data, IA, cloud), **presupuesto** y **modalidad**.
- Notifica por **Slack/Telegram/WhatsApp** si lo deseas.

## Ejecutar
```bash
pip install -r requirements.txt
cp .env.example .env
uvicorn app:app --reload --host 0.0.0.0 --port 8002
```

## Ejemplos
```
GET /recommend?bank=santander&area=ciberseguridad&budget=120000&modality=online
```

## Roadmap
- Conector a newsletters por **Gmail API**.
- Scrapers ligeros (RSS/API públicas) con `requests + BeautifulSoup`.
- Panel simple para marcar vistos/favoritos (SQLite + FastAPI).
