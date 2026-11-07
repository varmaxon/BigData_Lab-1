# Лабораторная работа — Мини-платформа данных

**Стек:** Postgres → Parquet → DuckDB → dbt  
**Время:** 1–2 часа  
**Уровень:** базовый

## Что строим

Упрощённую версию «малого масштаба» из семинара:

```
Postgres          →  Parquet (data/)  →  DuckDB  →  dbt models
(источник, OLTP)     (Raw Zone, лог)     (OLAP)      (трансформации)
```

## Структура

```
lab/
├── docker-compose.yml          # Postgres
├── requirements.txt
├── setup/
│   └── generate_data.py        # генерация данных + загрузка в Postgres
├── data/                       # Parquet файлы (создаются в ноутбуках)
├── notebooks/
│   ├── 01_ingestion.ipynb      # Postgres → Parquet
│   ├── 02_duckdb_analytics.ipynb  # SQL поверх Parquet
│   └── 03_dbt_models.ipynb     # dbt staging + marts
└── dbt_orders/                 # dbt-проект
    ├── models/staging/
    │   ├── stg_orders.sql      ← TODO: заполнить
    │   └── stg_customers.sql   ← готово
    └── models/marts/
        └── fct_revenue.sql     ← TODO: заполнить
```

## Быстрый старт

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Запуск Postgres

```bash
docker compose up -d
# Подождать ~10с пока поднимется
```

### 3. Генерация данных

```bash
python setup/generate_data.py
```

Создаёт:
- 120 клиентов в `raw_customers`
- 1500 заказов в `raw_orders`
- Parquet-файлы в `data/` (на случай если Postgres недоступен)

### 4. Запуск Jupyter

```bash
jupyter notebook notebooks/
```

Открывайте ноутбуки по порядку: 01 → 02 → 03.

---

## Если Postgres недоступен

Пропустите Notebook 01. Начните с Notebook 02 — данные в `data/*.parquet`  
уже создаются скриптом `setup/generate_data.py` даже без Postgres.

## Данные

Синтетический e-commerce датасет:

**raw_orders** (1500 строк)
| Поле | Тип | Описание |
|------|-----|----------|
| order_id | int | PK |
| customer_id | int | FK → customers |
| product | str | Название товара |
| category | str | Electronics / Clothing / Home / Sports / Books |
| quantity | int | Количество |
| unit_price | float | Цена за единицу (руб) |
| discount | float | Скидка (0–0.15) |
| amount | float | Итоговая сумма |
| status | str | pending / shipped / cancelled / returned |
| order_date | date | Дата заказа (2023) |
| created_at | timestamp | Время записи |

**raw_customers** (120 строк)
| Поле | Тип | Описание |
|------|-----|----------|
| customer_id | int | PK |
| name | str | Имя клиента |
| city | str | Город |
| segment | str | B2B / B2C |
| created_at | timestamp | Дата регистрации |

## Связь с семинаром

| Концепция из семинара | Реализация в лабораторной |
|----------------------|--------------------------|
| Лог vs Снапшот | `raw_orders.parquet` (лог) → `mart_revenue.parquet` (снапшот) |
| Parquet как формат хранения | Всё в `data/*.parquet` |
| DuckDB как OLAP | Notebook 02: запросы без сервера |
| dbt трансформации | Notebook 03: staging → mart |
| Граф зависимостей | `{{ ref() }}` в fct_revenue.sql |
| Тесты качества | `schema.yml`: not_null, unique, accepted_values |
