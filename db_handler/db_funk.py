from create_bot import pg_manager
from sqlalchemy import BigInteger, Text, Boolean, DateTime
from typing import List
import asyncio


async def create_users_table():
    columns = [
        {
            "name": "user_id",
            "type": BigInteger,
            "options": {
                "primary_key": True,
                "unique": True,
            },
        },
        {
            "name": "chat_id",
            "type": BigInteger,
        },
        {
            "name": "username",
            "type": Text,
        },
        {
            "name": "full_name",
            "type": Text,
        },
        {
            "name": "org_name",
            "type": Text,
        },
        {"name": "admin", "type": Boolean},
    ]
    async with pg_manager:
        await pg_manager.create_table(table_name="users", columns=columns)


async def create_documents_table():
    columns = [
        {
            "name": "id",
            "type": BigInteger,
            "options": {
                "primary_key": True,
                "unique": True,
            },
        },
        {
            "name": "user_id",
            "type": BigInteger,
        },
        {
            "name": "filename",
            "type": Text,
        },
        {
            "name": "load_date",
            "type": DateTime,
        },
        {
            "name": "period",
            "type": Text,
        },
        {"name": "admin", "type": Boolean},
    ]
    async with pg_manager:
        await pg_manager.create_table(table_name="documnets", columns=columns)


async def get_user_info(user_id: int):
    async with pg_manager:
        user_info = await pg_manager.select_data(
            table_name="users",
            where_dict={"user_id": user_id},
            one_dict=True,
        )
        if user_info:
            return user_info
        else:
            return None


async def insert_user(user_data: dict):
    async with pg_manager:
        await pg_manager.insert_data_with_update(
            table_name="users", records_data=user_data, conflict_column="user_id"
        )
