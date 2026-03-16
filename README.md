# Eduplat API

Backend образовательной платформы Eduplat. FastAPI + SQLAlchemy.

**Base URL:** `http://localhost:8000/api/v1`

Все защищённые эндпоинты (🔒) требуют заголовок:
```
Authorization: Bearer <access_token>
```

---

## Содержание

- [Auth](#auth)
- [Users](#users)
- [Profile — About](#profile--about)
- [Profile — Academic](#profile--academic)
- [Profile — Extracurricular](#profile--extracurricular)
- [Universities](#universities)
- [Opportunities](#opportunities)
- [Motivation Letter](#motivation-letter)

---

## Auth

### `POST /auth/register`

Регистрация нового пользователя.

**Body:**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "confirm_password": "password123"
}
```

**Response `201`:**
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

---

### `POST /auth/login`

Вход в аккаунт.

**Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response `200`:**
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

---

## Users

### `GET /users/me` 🔒

Получить полный профиль текущего пользователя.

**Response `200`:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "is_active": true,
  "created_at": "2024-01-01T12:00:00Z",
  "about": {
    "id": 1,
    "user_id": 1,
    "name": "Иван Иванов",
    "school": "Школа №1",
    "grade": "11",
    "updated_at": "2024-01-02T10:00:00Z"
  },
  "academic_info": {
    "id": 1,
    "user_id": 1,
    "gpa": 3.8,
    "sat": 1400,
    "ielts": 7.5,
    "toefl": null,
    "updated_at": "2024-01-02T10:00:00Z"
  },
  "extracurriculars": [
    {
      "id": 1,
      "user_id": 1,
      "category": "volunteering",
      "years_active": "2020-2023",
      "created_at": "2024-01-02T10:00:00Z"
    }
  ]
}
```

---

### `DELETE /users/me` 🔒

Удалить аккаунт текущего пользователя.

**Response `204` — No Content**

---

## Profile — About

### `POST /profile/about` 🔒

Создать или обновить личную информацию. Все поля опциональны.

**Body:**
```json
{
  "name": "Иван Иванов",
  "email": "newemail@example.com",
  "school": "Школа №1",
  "grade": "11"
}
```

**Response `201`:**
```json
{
  "id": 1,
  "user_id": 1,
  "name": "Иван Иванов",
  "school": "Школа №1",
  "grade": "11",
  "updated_at": "2024-01-02T10:00:00Z"
}
```

---

### `GET /profile/about` 🔒

Получить личную информацию текущего пользователя.

**Response `200`:** — аналогичен ответу `POST /profile/about`.

---

## Profile — Academic

### `POST /profile/academic` 🔒

Создать или обновить академическую информацию.

> Валидация: GPA `0.0–4.0`, SAT `400–1600`, IELTS `1.0–9.0`, TOEFL `0–120`

**Body:**
```json
{
  "gpa": 3.8,
  "sat": 1400,
  "ielts": 7.5,
  "toefl": null
}
```

**Response `201`:**
```json
{
  "id": 1,
  "user_id": 1,
  "gpa": 3.8,
  "sat": 1400,
  "ielts": 7.5,
  "toefl": null,
  "updated_at": "2024-01-02T10:00:00Z"
}
```

---

### `GET /profile/academic` 🔒

Получить академическую информацию текущего пользователя.

**Response `200`:** — аналогичен ответу `POST /profile/academic`.

---

## Profile — Extracurricular

### `POST /profile/extracurricular` 🔒

Заменить все внеклассные активности пользователя (предыдущие удаляются полностью).

> Доступные категории: `volunteering`, `leadership`, `club`, `research`, `olympiad`, `sport`  
> Формат `years_active`: `"YYYY"` или `"YYYY-YYYY"`

**Body:**
```json
{
  "categories": ["volunteering", "leadership", "olympiad"],
  "years_active": "2020-2024"
}
```

**Response `201`:**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "category": "volunteering",
    "years_active": "2020-2024",
    "created_at": "2024-01-02T10:00:00Z"
  },
  {
    "id": 2,
    "user_id": 1,
    "category": "leadership",
    "years_active": "2020-2024",
    "created_at": "2024-01-02T10:00:00Z"
  }
]
```

---

### `GET /profile/extracurricular` 🔒

Получить список всех внеклассных активностей пользователя.

**Response `200`:** — массив, аналогичный ответу `POST /profile/extracurricular`.

---

### `DELETE /profile/extracurricular/{entry_id}` 🔒

Удалить конкретную запись по ID.

**Response `204` — No Content**

**Response `404`:**
```json
{ "detail": "Запись не найдена" }
```

---

## Universities

### `GET /universities/` 🔒

Список университетов с расчётом шанса поступления на основе профиля пользователя.

**Query params (все опциональны):**

| Параметр | Тип | По умолчанию | Описание |
|---|---|---|---|
| `country` | string | — | Фильтр по стране: `США`, `Канада`, ... |
| `label` | string | — | Фильтр: `Сложно`, `Средне`, `Реально` |
| `sort_by` | string | `ranking` | `ranking`, `min_gpa`, `min_sat`, `min_ielts`, `probability` |
| `sort_order` | string | `asc` | `asc` или `desc` |

**Response `200`:**
```json
[
  {
    "id": 1,
    "name": "MIT",
    "country": "США",
    "city": "Кембридж",
    "min_gpa": 3.5,
    "min_sat": 1500,
    "probability": 12.5,
    "label": "Средне",
    "color": "yellow",
    "full_description": "Описание университета..."
  }
]
```

> `label` / `color`: `Сложно` / `red`, `Средне` / `yellow`, `Реально` / `green`

---

### `GET /universities/countries` 🔒

Список всех доступных стран.

**Response `200`:**
```json
["Австралия", "Великобритания", "Канада", "США"]
```

---

## Opportunities

### `GET /opportunities/` 🔒

Список стажировок, волонтёрств и хакатонов.

**Query params (опционально):**

| Параметр | Тип | Описание |
|---|---|---|
| `type` | string | `internship`, `volunteering`, `hackathon` |

**Response `200`:**
```json
[
  {
    "id": 1,
    "type": "hackathon",
    "title": "HackNU 2024",
    "short_description": "Международный хакатон в Алматы",
    "full_description": "Полное описание...",
    "image_url": "https://example.com/image.png",
    "event_date": "30 Сентября",
    "deadline": "23 Марта",
    "created_at": "2024-01-01T12:00:00Z"
  }
]
```

---

### `GET /opportunities/{opportunity_id}` 🔒

Получить одну возможность по ID.

**Response `200`:** — объект аналогичный элементу массива выше.

**Response `404`:**
```json
{ "detail": "Возможность не найдена" }
```

---

## Motivation Letter

### `POST /motivation-letter/analyze` 🔒

Отправить мотивационное письмо на AI-анализ (GPT-4o-mini).

> Минимум 100 символов, максимум 10 000 символов.

**Body:**
```json
{
  "text": "Я хочу поступить в этот университет, потому что..."
}
```

**Response `200`:**
```json
{
  "score": 7,
  "label": "Хорошо",
  "color": "yellow",
  "summary": "Письмо хорошо структурировано, но не хватает конкретных примеров.",
  "strengths": [
    "Чёткая структура с введением и заключением",
    "Выражена личная мотивация"
  ],
  "weaknesses": [
    "Нет конкретных достижений",
    "Использованы клишированные фразы"
  ],
  "suggestions": [
    "Добавьте конкретные примеры из вашего опыта",
    "Опишите, почему именно этот университет и направление"
  ]
}
```

> `label` / `color`: `Можно лучше` / `red` (1–4), `Хорошо` / `yellow` (5–8), `Отлично` / `green` (9–10)

---

## Коды ошибок

| Код | Описание |
|---|---|
| `400` | Некорректные данные (email занят, пароли не совпадают и т.д.) |
| `401` | Неверный токен или учётные данные |
| `403` | Аккаунт деактивирован |
| `404` | Ресурс не найден |
| `422` | Ошибка валидации (неверный формат данных) |