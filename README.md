# Проект: Marketplace для локальных продавцов (Simple Market) (не доделано)
**1. Ключевые сущности / фичи:**
- Пользователи: покупатели + продавцы (Auth-service, JWT).
- Товары: CRUD, картинки (Product-service).
- Заказы: создание, проверка стока, статус (Order-service).
- События: topic products (created/updated), topic orders (order_created, order_paid).
- UI (опционально): простой SPA или API-каллиграфия для тестов.
- Админ: базовые метрики/health.

**2. Микросервисы**
- auth-service — регистрация, логин, JWT, refresh token (Postgres).
- product-service — CRUD товаров, публикует события в Kafka, хранит свои товары (Postgres).
- order-service — создаёт заказы, подписывается на products (Kafka), хранит свои заказы и кеш товаров (Postgres).
- nginx — reverse-proxy / gateway (маршрутизация, TLS в будущем).
- kafka + zookeeper — event bus.
- Базы: отдельные Postgres-инстансы (или схемы для локальной dev простоты).
- (Опционально) worker-service — доставка/уведомления, DLQ.
