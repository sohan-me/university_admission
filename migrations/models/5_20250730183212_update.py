from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "country" ADD "description" TEXT;
        ALTER TABLE "university" ADD "description" TEXT;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "country" DROP COLUMN "description";
        ALTER TABLE "university" DROP COLUMN "description";"""
