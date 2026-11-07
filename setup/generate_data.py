"""
Генерация синтетических данных и загрузка в Postgres.
Запуск: python setup/generate_data.py

Создаёт:
  - таблицы raw_customers и raw_orders в Postgres
  - Parquet-файлы в data/ (если Postgres недоступен)
"""

import random
import datetime
import os
import pandas as pd
import sqlalchemy as sa

random.seed(42)

# ── параметры ─────────────────────────────────────────────────────────────────
N_CUSTOMERS = 120
N_ORDERS    = 1500
DB_URL      = os.getenv(
    "DATABASE_URL",
    "postgresql://analyst:analyst123@localhost:5432/orders_db",
)
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

# ── справочники ───────────────────────────────────────────────────────────────
CITIES = [
    "Москва", "Санкт-Петербург", "Новосибирск", "Екатеринбург",
    "Казань", "Нижний Новгород", "Челябинск", "Самара",
]
SEGMENTS   = ["B2C", "B2C", "B2C", "B2B"]       # B2C чаще
STATUSES   = ["pending", "shipped", "cancelled", "returned"]
STATUS_W   = [0.25, 0.55, 0.12, 0.08]
CATEGORIES = ["Electronics", "Clothing", "Home", "Sports", "Books"]
PRODUCTS   = {
    "Electronics": [("Ноутбук", 55000), ("Смартфон", 35000), ("Наушники", 8000)],
    "Clothing":    [("Куртка", 6500),   ("Кроссовки", 7200), ("Джинсы", 4500)],
    "Home":        [("Кофемашина", 12000), ("Пылесос", 9000), ("Чайник", 2500)],
    "Sports":      [("Велосипед", 28000), ("Гантели", 3500), ("Коврик", 1800)],
    "Books":       [("Книга 1", 600),   ("Книга 2", 800),   ("Книга 3", 450)],
}

# ── генерация customers ───────────────────────────────────────────────────────
def gen_customers(n: int) -> pd.DataFrame:
    rows = []
    for i in range(1, n + 1):
        created = datetime.date(2022, 1, 1) + datetime.timedelta(
            days=random.randint(0, 365)
        )
        rows.append({
            "customer_id": i,
            "name":        f"Клиент-{i:04d}",
            "city":        random.choice(CITIES),
            "segment":     random.choice(SEGMENTS),
            "created_at":  datetime.datetime.combine(created, datetime.time.min),
        })
    return pd.DataFrame(rows)

# ── генерация orders ──────────────────────────────────────────────────────────
def gen_orders(n: int, n_customers: int) -> pd.DataFrame:
    rows = []
    for i in range(1, n + 1):
        cat      = random.choice(CATEGORIES)
        name, price = random.choice(PRODUCTS[cat])
        qty      = random.randint(1, 3)
        discount = random.choice([0.0, 0.0, 0.05, 0.10, 0.15])
        amount   = round(price * qty * (1 - discount), 2)
        order_dt = datetime.date(2023, 1, 1) + datetime.timedelta(
            days=random.randint(0, 364)
        )
        created  = datetime.datetime.combine(
            order_dt,
            datetime.time(random.randint(6, 22), random.randint(0, 59)),
        )
        rows.append({
            "order_id":    i,
            "customer_id": random.randint(1, n_customers),
            "product":     name,
            "category":    cat,
            "quantity":    qty,
            "unit_price":  float(price),
            "discount":    discount,
            "amount":      amount,
            "status":      random.choices(STATUSES, STATUS_W)[0],
            "order_date":  order_dt,
            "created_at":  created,
        })
    return pd.DataFrame(rows)

# ── сохранение Parquet ────────────────────────────────────────────────────────
def save_parquet(customers: pd.DataFrame, orders: pd.DataFrame):
    os.makedirs(DATA_DIR, exist_ok=True)
    customers.to_parquet(os.path.join(DATA_DIR, "raw_customers.parquet"), index=False)
    orders.to_parquet(os.path.join(DATA_DIR, "raw_orders.parquet"), index=False)
    print(f"[parquet] raw_customers.parquet: {len(customers)} строк")
    print(f"[parquet] raw_orders.parquet:    {len(orders)} строк")

# ── загрузка в Postgres ───────────────────────────────────────────────────────
def load_postgres(customers: pd.DataFrame, orders: pd.DataFrame):
    engine = sa.create_engine(DB_URL)
    with engine.connect() as conn:
        customers.to_sql("raw_customers", conn, if_exists="replace",
                         index=False, schema="public")
        orders.to_sql("raw_orders", conn, if_exists="replace",
                      index=False, schema="public")
        conn.commit()
    print(f"[postgres] raw_customers: {len(customers)} строк")
    print(f"[postgres] raw_orders:    {len(orders)} строк")

# ── main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Генерация данных...")
    customers = gen_customers(N_CUSTOMERS)
    orders    = gen_orders(N_ORDERS, N_CUSTOMERS)

    save_parquet(customers, orders)

    try:
        load_postgres(customers, orders)
        print("\n✓ Данные загружены в Postgres и сохранены в data/")
    except Exception as e:
        print(f"\n⚠ Postgres недоступен ({e})")
        print("  Данные сохранены только в data/*.parquet")
        print("  Notebook 01 (Ingestion) можно пропустить — начните с Notebook 02.")
