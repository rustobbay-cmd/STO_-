from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

import aiosqlite


@dataclass(slots=True)
class Order:
    id: int
    user_id: int
    name: str
    phone: str
    car: str
    issue: str
    service: str
    date: str
    time: str
    duration: int


class Database:
    def __init__(self, path: str):
        self.path = path

    async def init(self) -> None:
        async with aiosqlite.connect(self.path) as db:
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    car TEXT NOT NULL,
                    issue TEXT NOT NULL,
                    service TEXT NOT NULL,
                    date TEXT NOT NULL,
                    time TEXT NOT NULL,
                    duration INTEGER NOT NULL
                )
                """
            )
            await db.commit()

    async def add_order(
        self,
        user_id: int,
        name: str,
        phone: str,
        car: str,
        issue: str,
        service: str,
        date: str,
        time: str,
        duration: int,
    ) -> None:
        async with aiosqlite.connect(self.path) as db:
            await db.execute(
                """
                INSERT INTO orders (user_id, name, phone, car, issue, service, date, time, duration)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (user_id, name, phone, car, issue, service, date, time, duration),
            )
            await db.commit()

    async def list_user_orders(self, user_id: int) -> list[Order]:
        async with aiosqlite.connect(self.path) as db:
            cursor = await db.execute(
                "SELECT id, user_id, name, phone, car, issue, service, date, time, duration FROM orders WHERE user_id = ? ORDER BY date, time",
                (user_id,),
            )
            rows = await cursor.fetchall()
        return [Order(*row) for row in rows]

    async def list_all_orders(self) -> list[Order]:
        async with aiosqlite.connect(self.path) as db:
            cursor = await db.execute(
                "SELECT id, user_id, name, phone, car, issue, service, date, time, duration FROM orders ORDER BY date, time"
            )
            rows = await cursor.fetchall()
        return [Order(*row) for row in rows]

    async def delete_order(self, order_id: int) -> None:
        async with aiosqlite.connect(self.path) as db:
            await db.execute("DELETE FROM orders WHERE id = ?", (order_id,))
            await db.commit()

    async def extend_order(self, order_id: int, hours: int = 1) -> None:
        async with aiosqlite.connect(self.path) as db:
            await db.execute("UPDATE orders SET duration = duration + ? WHERE id = ?", (hours, order_id))
            await db.commit()

    async def busy_slots(self, date_str: str) -> list[str]:
        async with aiosqlite.connect(self.path) as db:
            cursor = await db.execute("SELECT time, duration FROM orders WHERE date = ?", (date_str,))
            rows = await cursor.fetchall()

        busy: list[str] = []
        for time_value, duration in rows:
            try:
                start_hour = int(str(time_value).split(":")[0])
                for offset in range(int(duration)):
                    busy.append(f"{start_hour + offset}:00")
            except (ValueError, TypeError):
                continue
        return busy

    async def has_free_slots(self, date_str: str, duration: int, start_hour: int, end_hour: int) -> bool:
        busy = await self.busy_slots(date_str)
        now = datetime.now()
        current_hour = now.hour
        is_today = date_str == now.strftime("%d.%m")

        for hour in range(start_hour, end_hour):
            if is_today and hour <= current_hour:
                continue
            can_fit = True
            for offset in range(duration):
                check_hour = hour + offset
                if check_hour >= end_hour or f"{check_hour}:00" in busy:
                    can_fit = False
                    break
            if can_fit:
                return True
        return False

    async def available_times(self, date_str: str, duration: int, start_hour: int, end_hour: int) -> list[str]:
        busy = await self.busy_slots(date_str)
        now = datetime.now()
        current_hour = now.hour
        is_today = date_str == now.strftime("%d.%m")

        result: list[str] = []
        for hour in range(start_hour, end_hour):
            if is_today and hour <= current_hour:
                continue
            can_fit = True
            for offset in range(duration):
                check_hour = hour + offset
                if check_hour >= end_hour or f"{check_hour}:00" in busy:
                    can_fit = False
                    break
            if can_fit:
                result.append(f"{hour}:00")
        return result
