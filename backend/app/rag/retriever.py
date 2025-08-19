from typing import List, Dict


def _tokenize(text: str) -> List[str]:
    return [t.lower() for t in text.split() if t.strip()]


def _bow_vector(tokens: List[str]):
    counts = {}
    for t in tokens:
        counts[t] = counts.get(t, 0) + 1
    norm = sum(v * v for v in counts.values()) ** 0.5 or 1.0
    return {k: v / norm for k, v in counts.items()}


def _cosine(a: dict, b: dict) -> float:
    keys = a.keys() & b.keys()
    return sum(a[k] * b[k] for k in keys)


KB_ITEMS: List[Dict[str, str]] = [
    {
        "title": "Squat",
        "text": "The squat targets quads, glutes, and core. Keep chest up, push hips back, and track knees over toes.",
    },
    {
        "title": "Bench Press",
        "text": "Bench press works chest, triceps, and shoulders. Maintain scapular retraction and full foot contact.",
    },
    {
        "title": "Protein Intake",
        "text": "Aim for 1.6-2.2 g/kg/day of protein for muscle gain. Distribute across 3-4 meals with 20-40g each.",
    },
    {
        "title": "Recovery",
        "text": "Sleep 7-9 hours and manage stress. Incorporate deload weeks and light activity for recovery.",
    },
    {
        "title": "Injury Prevention",
        "text": "Warm up 5-10 minutes, use proper technique, and progress loads gradually to avoid injuries.",
    },
]

KB_VECTORS = [_bow_vector(_tokenize(item["text"])) for item in KB_ITEMS]


def retrieve_context(query: str, k: int = 3) -> List[dict]:
    qv = _bow_vector(_tokenize(query))
    scored = [(_cosine(qv, v), i) for i, v in enumerate(KB_VECTORS)]
    scored.sort(reverse=True)
    top = [KB_ITEMS[i] for _, i in scored[:k]]
    return top



