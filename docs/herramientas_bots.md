# 🧰 Herramientas Técnicas para Crear Bots Automatizados

Guía práctica de **stacks**, librerías, servicios y buenas prácticas para construir:
- Bots **rule-based**
- Bots con **IA conversacional (NLP/LLM)**
- Flujos de **automatización** (recordatorios, tickets, notificaciones)

---

## 🏗️ Arquitectura de referencia (modular)


---


---

## 🧩 Catálogo de herramientas por capa

### 1) Canales (entrada/salida)
- **WhatsApp**: Twilio WhatsApp API / WhatsApp Cloud API
- **Telegram**: Bot API oficial
- **Slack**: Slack Bolt SDK (Python/JS)
- **Web**: Chat embebido (WebSocket/REST) con frontend (React, Web Components)

### 2) Webhooks / Backend
- **Python**: FastAPI (rápido, tipado y async), Flask (mínimo)
- **Node.js**: Express, NestJS
- **Mensajería interna (opcional)**: Celery (Python), BullMQ (Node) para jobs/colas

### 3) NLU / IA Conversacional
- **Rule-based**: `rasa rules`, Botpress flows, regex/intents simples
- **NLU Clásico**: Rasa NLU (DIETClassifier), spaCy (entidades), Duckling (fechas/montos)
- **LLM Orchestration**: LangChain, LlamaIndex
- **LLM Providers**: OpenAI, Anthropic, Cohere, Google (Gemini), Open-source (Ollama + Llama 3, Mistral)
- **Embeddings/Vector DB (RAG)**: sentence-transformers / OpenAI embeddings + Chroma/FAISS/Pinecone/Weaviate

### 4) Automatización / Integraciones
- **Calendario**: Google Calendar API
- **Correo**: Gmail API
- **Mensajería**: Twilio (WhatsApp/SMS), Slack Web API, Telegram Bot API
- **Productividad**: Notion API, Google Sheets API, Trello API, Jira API
- **No-Code/Low-Code**: n8n (self-host), Make/Zapier (SaaS)

### 5) Persistencia / Estado
- **Base de datos**: PostgreSQL (estado de conversación, usuarios, tareas)
- **Cache/Cola**: Redis (sesiones, throttling, jobs)
- **Archivos**: S3 compatible (MinIO, AWS S3) para adjuntos
- **Vector DB**: Chroma (local), Pinecone/Weaviate (gestionados)

### 6) Observabilidad y MLOps
- **Logs/Métricas**: Prometheus + Grafana, ELK/Opensearch, Sentry
- **Trazas LLM**: Langfuse, OpenTelemetry
- **Evaluación de prompts/NLU**: Ragas (RAG), Rasa test stories, Botium

### 7) Seguridad
- **Secretos**: `.env` + Vault (1Password, Doppler, AWS Secrets Manager)
- **Auth**: OAuth2/OIDC si expones panel; firmas HMAC en webhooks
- **PII**: enmascarado, retención mínima, cifrado at-rest (Postgres + TLS)
- **Rate limiting**: nginx/Traefik + Redis
- **Auditoría**: logs de acciones y decisiones del bot

---

## 🧱 Stacks recomendados (según objetivo)

| Objetivo | Stack mínimo | Por qué |
|---|---|---|
| **Rule-based rápido** | Botpress o n8n + Telegram/Twilio | Arranque veloz, flujos visuales, bajo código |
| **IA conversacional (NLP + reglas)** | Rasa (Core+NLU) + FastAPI + Postgres/Redis | Intents/slots, diálogos con estado, productivo |
| **LLM + RAG** | FastAPI + LangChain/LlamaIndex + Chroma/Pinecone + Twilio/Slack | Respuestas contextuales, docs de empresa |
| **Automatización de tareas** | FastAPI + Google Calendar/Sheets + n8n/Twilio | Recordatorios, reportes y notificaciones |

---

## 📦 Estructura de proyecto (Python, productivo)


