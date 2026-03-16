import os
from openai import OpenAI
from app.schemas.motivation_letter import MotivationLetterRequest, MotivationLetterResponse

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """Ты — эксперт по оценке мотивационных писем для поступления в университет. 
Твоя задача — объективно и строго оценить мотивационное письмо абитуриента.

Оценивай по следующим критериям:
1. **Структура и логика** — есть ли чёткое введение, основная часть и заключение
2. **Конкретность** — приведены ли реальные примеры, достижения, факты
3. **Мотивация** — понятно ли, почему абитуриент хочет учиться именно в этом направлении
4. **Уникальность** — выделяется ли письмо, есть ли личный голос
5. **Грамотность и стиль** — профессиональный ли язык, нет ли клише
6. **Релевантность** — соответствует ли содержание академическим требованиям

Выставь оценку от 1 до 10, где:
- 1–4: письмо слабое, требует серьёзной доработки
- 5–8: письмо хорошее, но есть точки роста
- 9–10: письмо отличное, почти идеально

Отвечай СТРОГО в формате JSON без каких-либо пояснений вне JSON:
{
  "score": <число от 1 до 10>,
  "summary": "<краткое резюме на 1–2 предложения>",
  "strengths": ["<сильная сторона 1>", "<сильная сторона 2>"],
  "weaknesses": ["<слабая сторона 1>", "<слабая сторона 2>"],
  "suggestions": ["<конкретный совет по улучшению 1>", "<конкретный совет 2>"]
}"""


def _get_label_and_color(score: int) -> tuple[str, str]:
    if score <= 4:
        return "Можно лучше", "red"
    elif score <= 8:
        return "Хорошо", "yellow"
    else:
        return "Отлично", "green"


class MotivationLetterService:
    def analyze(self, payload: MotivationLetterRequest) -> MotivationLetterResponse:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Оцени следующее мотивационное письмо:\n\n{payload.text}"},
            ],
            temperature=0.3,
            response_format={"type": "json_object"},
        )

        import json
        result = json.loads(response.choices[0].message.content)

        score = int(result["score"])
        score = max(1, min(10, score))
        label, color = _get_label_and_color(score)

        return MotivationLetterResponse(
            score=score,
            label=label,
            color=color,
            summary=result.get("summary", ""),
            strengths=result.get("strengths", []),
            weaknesses=result.get("weaknesses", []),
            suggestions=result.get("suggestions", []),
        )