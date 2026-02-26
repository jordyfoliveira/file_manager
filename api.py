from __future__ import annotations

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from text_analysis import top_words, top_words_format

app = FastAPI(title="Text Analyzer API", version="1.0.0")


class AnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=1)
    n: int = Field(10, ge=1, le=100)


class AnalyzeResponse(BaseModel):
    n: int
    report: str
    items: list[dict]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(req: AnalyzeRequest):
    text = req.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="text vazio")

    report = top_words_format(text, req.n)
    pairs = top_words(text, req.n)

    items = [{"rank": i, "word": w, "count": c} for i, (w, c) in enumerate(pairs, 1)]
    return {"n": req.n, "report": report, "items": items}