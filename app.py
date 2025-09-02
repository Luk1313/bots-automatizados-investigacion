from fastapi import FastAPI
from pydantic import BaseModel
from recommender import recommend
from notifiers import notify_slack, notify_telegram, notify_whatsapp

app = FastAPI(title="EduDealsBot")

class Query(BaseModel):
    bank: str
    area: str | None = None
    budget: int | None = None
    modality: str | None = "online"
    notify: bool = False

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/recommend")
def rec(bank: str, area: str | None = None, budget: int | None = None, modality: str | None = "online", notify: bool = False):
    items = recommend(bank, area, budget, modality)
    if notify and items:
        lines = [f"🎓 {o.title} – {o.provider} (${o.price_clp} CLP, -{o.discount_pct}%) {o.url}" for o in items[:5]]
        text = "*Recomendaciones educacionales:*
" + "\n".join(lines)
        notify_slack(text); notify_telegram(text); notify_whatsapp(text)
    return {"results": [o.dict() for o in items]}
