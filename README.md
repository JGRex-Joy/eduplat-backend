# Eduplat API — документация для фронтенда

Base URL: `https://your-service.onrender.com/api/v1`  
Локально: `http://localhost:8000/api/v1`

Все запросы и ответы — **JSON**.  
Защищённые эндпоинты требуют заголовок:
```
Authorization: Bearer <access_token>
```

---

## Auth

### POST `/auth/register`
Регистрация нового пользователя.

**Body:**
```json
{
  "email": "user@example.com",
  "password": "mypassword123",
  "confirm_password": "mypassword123"
}
```

**Response `201`:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Ошибки:**
```json
{ "detail": "Пользователь с таким email уже существует" }
```

---

### POST `/auth/login`
Вход в аккаунт.

**Body:**
```json
{
  "email": "user@example.com",
  "password": "mypassword123"
}
```

**Response `200`:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Ошибки:**
```json
{ "detail": "Неверный email или пароль" }
{ "detail": "Аккаунт деактивирован" }
```

---

## Users

### GET `/users/me` 🔒
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
    "name": "Алибек",
    "school": "НИШ Алматы",
    "grade": "11",
    "updated_at": "2024-01-02T10:00:00Z"
  },
  "academic_info": {
    "id": 1,
    "user_id": 1,
    "gpa": 3.9,
    "sat": 1450,
    "ielts_toefl": 7.5,
    "act": 32,
    "updated_at": "2024-01-02T10:00:00Z"
  },
  "extracurriculars": [
    {
      "id": 1,
      "user_id": 1,
      "category": "leadership",
      "years_active": "2022-2024",
      "created_at": "2024-01-02T10:00:00Z"
    }
  ]
}
```

> Поля `about`, `academic_info` могут быть `null` если ещё не заполнены.  
> `extracurriculars` — пустой массив `[]` если нет записей.

---

### DELETE `/users/me` 🔒
Удалить аккаунт.

**Response `204`** — пустой ответ.

---

## Profile

### POST `/profile/about` 🔒
Создать или обновить информацию "О себе".  
Можно передавать только те поля которые хочешь обновить.

**Body:**
```json
{
  "name": "Алибек",
  "email": "newemail@example.com",
  "school": "НИШ Алматы",
  "grade": "11"
}
```

**Response `201`:**
```json
{
  "id": 1,
  "user_id": 1,
  "name": "Алибек",
  "school": "НИШ Алматы",
  "grade": "11",
  "updated_at": "2024-01-02T10:00:00Z"
}
```

**Ошибки:**
```json
{ "detail": "Этот email уже используется другим пользователем" }
```

---

### GET `/profile/about` 🔒
Получить информацию "О себе".

**Response `200`:**
```json
{
  "id": 1,
  "user_id": 1,
  "name": "Алибек",
  "school": "НИШ Алматы",
  "grade": "11",
  "updated_at": "2024-01-02T10:00:00Z"
}
```

**Ошибки:**
```json
{ "detail": "Информация не найдена" }
```

---

### POST `/profile/academic` 🔒
Создать или обновить академические данные.  
Все поля опциональны — передавай только нужные.

**Body:**
```json
{
  "gpa": 3.9,
  "sat": 1450,
  "ielts_toefl": 7.5,
  "act": 32
}
```

Допустимые диапазоны:
- `gpa` — от `0.0` до `4.0`
- `sat` — от `400` до `1600`
- `ielts_toefl` — от `0` до `120`
- `act` — от `1` до `36`

**Response `201`:**
```json
{
  "id": 1,
  "user_id": 1,
  "gpa": 3.9,
  "sat": 1450,
  "ielts_toefl": 7.5,
  "act": 32,
  "updated_at": "2024-01-02T10:00:00Z"
}
```

---

### GET `/profile/academic` 🔒
Получить академические данные.

**Response `200`:**
```json
{
  "id": 1,
  "user_id": 1,
  "gpa": 3.9,
  "sat": 1450,
  "ielts_toefl": 7.5,
  "act": 32,
  "updated_at": "2024-01-02T10:00:00Z"
}
```

**Ошибки:**
```json
{ "detail": "Академическая информация не найдена" }
```

---

### POST `/profile/extracurricular` 🔒
Заменить все активности пользователя.  
⚠️ Каждый вызов **полностью перезаписывает** предыдущий список.

**Body:**
```json
{
  "categories": ["leadership", "research", "sport"],
  "years_active": "2022-2024"
}
```

Доступные категории для `categories`:
| Значение | Описание |
|---|---|
| `volunteering` | Волонтёрство |
| `leadership` | Лидерство |
| `club` | Клуб / кружок |
| `research` | Исследования |
| `olympiad` | Олимпиады |
| `sport` | Спорт |

Формат `years_active`: `"YYYY"` или `"YYYY-YYYY"` (например `"2023"` или `"2021-2024"`). Можно передать `null`.

**Response `201`:**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "category": "leadership",
    "years_active": "2022-2024",
    "created_at": "2024-01-02T10:00:00Z"
  },
  {
    "id": 2,
    "user_id": 1,
    "category": "research",
    "years_active": "2022-2024",
    "created_at": "2024-01-02T10:00:00Z"
  },
  {
    "id": 3,
    "user_id": 1,
    "category": "sport",
    "years_active": "2022-2024",
    "created_at": "2024-01-02T10:00:00Z"
  }
]
```

---

### GET `/profile/extracurricular` 🔒
Получить список всех активностей.

**Response `200`:**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "category": "leadership",
    "years_active": "2022-2024",
    "created_at": "2024-01-02T10:00:00Z"
  }
]
```

---

### DELETE `/profile/extracurricular/{id}` 🔒
Удалить одну активность по ID.

**Response `204`** — пустой ответ.

**Ошибки:**
```json
{ "detail": "Запись не найдена" }
```

---

## Общие ошибки

| Статус | Когда |
|---|---|
| `400` | Неверные данные в запросе |
| `401` | Токен отсутствует или недействителен |
| `403` | Доступ запрещён |
| `404` | Объект не найден |
| `422` | Ошибка валидации (неверный формат полей) |

Ошибка валидации `422` выглядит так:
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```