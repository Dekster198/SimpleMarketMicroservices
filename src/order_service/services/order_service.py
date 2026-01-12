from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from src.order_service.kafka.producer import send_event
from src.order_service.models import Order, OrderStatus, OrderItem


class OrderService:
    @staticmethod
    async def create_order(
            session: AsyncSession,
            buyer_id: int,
            items: list[dict]
    ):
        order = Order(
            buyer_id=buyer_id,
            status=OrderStatus.NEW
        )
        session.add(order)
        await session.flush()  # до flush в записи Order не было id, после flush есть

        order_items = []
        for item in items:
            order_items.append(
                OrderItem(
                    order_id=order.id,
                    product_id=item['product_id'],
                    quantity=item['quantity']
                )
            )

        session.add_all(order_items)
        await session.commit()

        await send_event(
            topic='order.created',
            value={
                'event': 'order_created',
                'order_id': order.id,
                'buyer_id': buyer_id,
                'items': items,
                'created_at': datetime.now(timezone.utc).isoformat()
            }
        )

        return order
