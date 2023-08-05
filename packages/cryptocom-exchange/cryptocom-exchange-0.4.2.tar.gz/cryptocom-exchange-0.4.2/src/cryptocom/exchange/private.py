import asyncio

from typing import List, Dict

from .api import ApiProvider, ApiError
from .structs import (
    Pair, OrderSide, OrderStatus, OrderType, Order, Coin, Balance,
    OrderExecType, OrderForceType, PrivateTrade
)


class Account:
    """Provides access to account actions and data. Balance, trades, orders."""
    def __init__(
            self, *, api_key: str = '', api_secret: str = '',
            from_env: bool = False, api: ApiProvider = None):
        if not api and not (api_key and api_secret) and not from_env:
            raise ValueError(
                'Pass ApiProvider or api_key with api_secret or from_env')
        self.api = api or ApiProvider(
            api_key=api_key, api_secret=api_secret, from_env=from_env)

    async def get_balance(self) -> Dict[Coin, Balance]:
        """Return balance."""
        data = await self.api.post(
            'private/get-account-summary', {'params': {}})
        return {
            Coin(bal['currency']): Balance(
                total=bal['balance'],
                available=bal['available'],
                in_orders=bal['order'],
                in_stake=bal['stake'],
                coin=Coin(bal['currency'])
            ) for bal in data['accounts']
        }

    async def get_orders_history(
            self, pair: Pair, page: int = 0,
            page_size: int = 200) -> List[Order]:
        """Return all history orders."""
        data = await self.api.post('private/get-order-history', {
            'params': {
                'instrument_name': pair.value,
                'page_size': page_size,
                'page': page
            }
        })
        return [
            Order.create_from_api(order)
            for order in data.get('order_list') or []
        ]

    async def get_open_orders(
            self, pair: Pair, page: int = 0,
            page_size: int = 200) -> List[Order]:
        """Return open orders."""
        data = await self.api.post('private/get-open-orders', {
            'params': {
                'instrument_name': pair.value,
                'page_size': page_size,
                'page': page
            }
        })
        return [
            Order.create_from_api(order)
            for order in data.get('order_list') or []
        ]

    async def get_trades(
            self, pair: Pair, page: int = 0,
            page_size: int = 200)  -> List[PrivateTrade]:
        """Return trades."""
        data = await self.api.post('private/get-trades', {
            'params': {
                'instrument_name': pair.value,
                'page_size': page_size,
                'page': page
            }
        })
        return [
            PrivateTrade.create_from_api(trade)
            for trade in data.get('trade_list') or []
        ]

    async def create_order(
            self, pair: Pair, side: OrderSide, type_: OrderType,
            quantity: float, price: float = 0,
            force_type: OrderForceType = None,
            exec_type: OrderExecType = None,
            client_id: int = None) -> int:
        """Create raw order with buy or sell side."""
        data = {
            'instrument_name': pair.value, 'side': side.value,
            'type': type_.value
        }

        if type_ == OrderType.MARKET and side == OrderSide.BUY:
            data['notional'] = quantity
        else:
            data['quantity'] = quantity

        if client_id:
            data['client_oid'] = str(client_id)

        if price:
            if type_ == OrderType.MARKET:
                raise ValueError(
                    "Error, MARKET execution do not support price value")
            data['price'] = price

        resp = await self.api.post('private/create-order', {'params': data})
        return int(resp['order_id'])

    async def buy_limit(
            self, pair: Pair, quantity: float, price: float,
            force_type: OrderForceType = None,
            exec_type: OrderExecType = None,
            client_id: int = None) -> int:
        """Buy limit order."""
        return await self.create_order(
            pair, OrderSide.BUY, OrderType.LIMIT, quantity, price
        )

    async def sell_limit(
            self, pair: Pair, quantity: float, price: float,
            force_type: OrderForceType = None,
            exec_type: OrderExecType = None,
            client_id: int = None) -> int:
        """Sell limit order."""
        return await self.create_order(
            pair, OrderSide.SELL, OrderType.LIMIT, quantity, price
        )

    async def wait_for_status(
            self, order_id: int, statuses, delay: int = 0.1) -> None:
        """Wait for order status."""
        order = await self.get_order(order_id)

        for _ in range(self.api.retries):
            if order.status in statuses:
                break

            await asyncio.sleep(delay)
            order = await self.get_order(order_id)

        if order.status not in statuses:
            raise ApiError(
                f"Status not changed for: {order}, must be in: {statuses}")

    async def buy_market(
            self, pair: Pair, spend: float, wait_for_fill=False) -> int:
        """Buy market order."""
        order_id = await self.create_order(
            pair, OrderSide.BUY, OrderType.MARKET, spend
        )
        if wait_for_fill:
            await self.wait_for_status(order_id, (
                OrderStatus.FILLED, OrderStatus.CANCELED, OrderStatus.EXPIRED,
                OrderStatus.REJECTED
            ))

        return order_id

    async def sell_market(
            self, pair: Pair, quantity: float, wait_for_fill=False) -> int:
        """Sell market order."""
        order_id = await self.create_order(
            pair, OrderSide.SELL, OrderType.MARKET, quantity
        )

        if wait_for_fill:
            await self.wait_for_status(order_id, (
                OrderStatus.FILLED, OrderStatus.CANCELED, OrderStatus.EXPIRED,
                OrderStatus.REJECTED
            ))

        return order_id

    async def get_order(self, order_id: int) -> Order:
        """Get order info."""
        data = await self.api.post('private/get-order-detail', {
            'params': {'order_id': str(order_id)}
        })
        return Order.create_from_api(data['order_info'])

    async def cancel_order(
            self, order_id: int, pair: Pair, check_status=False) -> None:
        """Cancel order."""
        await self.api.post('private/cancel-order', {
            'params': {'order_id': order_id, 'instrument_name': pair.value}
        })

        if not check_status:
            return

        await self.wait_for_status(order_id, (
            OrderStatus.CANCELED, OrderStatus.EXPIRED, OrderStatus.REJECTED
        ))

    async def cancel_open_orders(self, pair: Pair) -> None:
        """Cancel all open orders."""
        return await self.api.post('private/cancel-all-orders', {
            'params': {'instrument_name': pair.value}
        })

    async def listen_balance(self) -> Balance:
        async for data in self.api.listen(
                'user', 'user.balance', sign=True):
            for bal in data.get('data', []):
                yield Balance(
                    total=bal['balance'],
                    available=bal['available'],
                    in_orders=bal['order'],
                    in_stake=bal['stake'],
                    coin=Coin(bal['currency'])
                )

    async def listen_orders(self, pair: Pair) -> Order:
        async for data in self.api.listen(
                'user', f'user.order.{pair.value}', sign=True):
            for order in data.get('data', []):
                yield Order.create_from_api(order)
