# Planetarium Booking API

REST API для системи онлайн-бронювання квитків на астрономічні шоу у планетарії. Система дозволяє адмініструвати шоу, куполи, сесії, теми шоу, бронювання, квитки та користувачів. Зареєстровані користувачі можуть переглядати розклад, бронювати місця та переглядати свою історію бронювань.

## ✨ Основні функції

- CRUD операції для всіх моделей: AstronomyShow, ShowTheme, PlanetariumDome, ShowSession, Ticket, Reservation
- Реєстрація, автентифікація (JWT) та авторизація користувачів (email як логін)
- Кастомний профіль користувача (`/api/users/me/`)
- Перегляд розкладу шоу з можливістю фільтрації та пошуку (за темами, куполами, датами, назвою)
- Бронювання квитків з вибором конкретних місць та валідацією зайнятих місць
- Перегляд історії бронювань та квитків користувача (тільки своїх)
- Адміністративний доступ для повного керування даними
- Кастомні endpoints: доступні місця, місткість куполу, сесії куполу, завантаження зображень до шоу
- Автоматична документація API (Swagger/Redoc)
- Оптимізовані запити до БД (`select_related`/`prefetch_related`)
- Покриття тестами основних сценаріїв (pytest)

## 🛠️ Технології та стек

- **Backend:** Python, Django, Django REST Framework
- **База даних:** SQLite (для розробки), PostgreSQL (рекомендовано для production)
- **Автентифікація:** djangorestframework-simplejwt (JWT)
- **Фільтрація:** django-filter
- **Документація API:** drf-yasg (Swagger/Redoc)
- **Тестування:** pytest, pytest-django
- **Форматування коду:** black, isort, flake8

## 🚀 Налаштування та запуск

### Передумови

- Python 3.10+
- pip

### Інсталяція

1.  **Клонуйте репозиторій:**

    ```bash
    git clone <your-repository-url>
    cd Planetarium-api
    ```

2.  **Створіть та активуйте віртуальне середовище:**

    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Встановіть залежності:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Застосуйте міграції:**

    ```bash
    python manage.py migrate
    ```

5.  **Створіть суперкористувача (для доступу до адмінки та повних прав):**

    ```bash
    python manage.py createsuperuser
    ```

6.  **Запустіть сервер розробки:**
    ```bash
    python manage.py runserver
    ```
    API буде доступне за адресою `http://127.0.0.1:8000/api/`.

## ✅ Запуск тестів

Для запуску тестів виконайте команду в корені проекту (з активованим віртуальним середовищем):

```bash
pytest --ds=config.settings -v
```

## 📚 Документація API

Після запуску сервера, документація API доступна за адресами:

- **Swagger UI:** `http://127.0.0.1:8000/api/docs/`
- **ReDoc:** `http://127.0.0.1:8000/api/redoc/`

## 🔗 Основні ендпоінти

### Аутентифікація і користувачі

- `POST /api/users/register/` - Реєстрація
- `POST /api/users/token/` - Отримання JWT токена (логін)
- `POST /api/users/token/refresh/` - Оновлення JWT токена
- `GET/PUT/PATCH /api/users/me/` - Профіль поточного користувача
- `GET /api/users/` - Список користувачів (тільки для адміна)

### Шоу та теми

- `GET/POST /api/astronomy-shows/` - Список/Створення шоу
- `GET/PUT/PATCH/DELETE /api/astronomy-shows/{id}/` - Деталі/Оновлення/Видалення шоу
- `POST /api/astronomy-shows/{id}/upload-image/` - Завантаження зображення (тільки адмін)
- `GET/POST /api/show-themes/` - Список/Створення тем
- `GET/PUT/PATCH/DELETE /api/show-themes/{id}/` - Деталі/Оновлення/Видалення теми

### Куполи

- `GET/POST /api/planetarium-domes/` - Список/Створення куполів
- `GET/PUT/PATCH/DELETE /api/planetarium-domes/{id}/` - Деталі/Оновлення/Видалення куполу
- `GET /api/planetarium-domes/{id}/sessions/` - Список сесій для куполу
- `GET /api/planetarium-domes/{id}/capacity/` - Місткість куполу

### Сесії шоу

- `GET/POST /api/show-sessions/` - Список/Створення сесій
- `GET/PUT/PATCH/DELETE /api/show-sessions/{id}/` - Деталі/Оновлення/Видалення сесії
- `GET /api/show-sessions/{id}/available-seats/` - Список доступних місць

### Бронювання та квитки

- `GET/POST /api/reservations/` - Список/Створення бронювань (користувач бачить тільки свої)
- `GET /api/reservations/{id}/` - Деталі бронювання (тільки власник або адмін)
- `GET /api/tickets/` - Список квитків (користувач бачить тільки свої)
- `GET /api/tickets/{id}/` - Деталі квитка (тільки власник або адмін)
