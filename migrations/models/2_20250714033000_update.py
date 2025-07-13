from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "studentapplicationdocuments";
        DROP TABLE IF EXISTS "studentadmissionapplication";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
