from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import json, os

DATA_DIR = os.path.join(os.path.dirname(__file__), "data", "offers")

class Offer(BaseModel):
    provider: str
    title: str
    url: str
    modality: str
    price_clp: int
    discount_pct: int
    tags: List[str]

def load_offers(bank: str) -> List[Offer]:
    path = os.path.join(DATA_DIR, f"{bank}.json")
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [Offer(**o) for o in data]

def recommend(bank: str, area: Optional[str], budget: Optional[int], modality: Optional[str]) -> List[Offer]:
    items = load_offers(bank)
    def ok(o: Offer) -> bool:
        cond = True
        if area:
            cond = cond and (area.lower() in " ".join(o.tags + [o.title]).lower())
        if budget is not None:
            cond = cond and (o.price_clp <= budget)
        if modality:
            cond = cond and (o.modality.lower() == modality.lower())
        return cond
    return [o for o in items if ok(o)]
