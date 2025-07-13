from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "studentadmissionapplication" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "name" VARCHAR(100) NOT NULL,
    "phone" VARCHAR(20) NOT NULL,
    "email" VARCHAR(100),
    "residence_country" VARCHAR(50) NOT NULL,
    "interest_country" VARCHAR(50) NOT NULL,
    "intake_interest" VARCHAR(200) NOT NULL,
    "last_graduation" VARCHAR(200) NOT NULL,
    "interested_course" VARCHAR(200) NOT NULL,
    "current_stage" VARCHAR(200)
);
        CREATE TABLE IF NOT EXISTS "studentapplicationdocuments" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "passport" VARCHAR(300),
    "last_graduation_certificate" VARCHAR(300),
    "admission_application_id" INT NOT NULL UNIQUE REFERENCES "studentadmissionapplication" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "studentapplicationdocuments";
        DROP TABLE IF EXISTS "studentadmissionapplication";"""
