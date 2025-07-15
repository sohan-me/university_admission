from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "agentadmissionapplication" ADD "status" VARCHAR(21) NOT NULL DEFAULT 'New' /* NEW: New\nREVIEW: Review\nCOMMISSION_PAID: Commission Paid\nREJECTED: Rejected\nCONDITIONALOFFER: Conditional Offer\nUNCONDITIONALOFFER: Unconditional Offer\nCASDOCUMENTPENDING: CAS Documents Pending\nCASINTERVIEWPENDING: CAS InterView Pending\nCASINTERVIEWPASSED: CAS InterView Passed\nCASRECEIVED: CAS Received\nAPPLYFORVISA: Apply For Visa\nVISARECEIVED: Visa Received\nENROLLEMENTPENDING: Enrollement Pending\nENROLLEMENTCOMPLETE: Enrollement Complete */;
        CREATE TABLE IF NOT EXISTS "agentapplicationcommission" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "student_fee" INT NOT NULL DEFAULT 0,
    "commission" INT NOT NULL DEFAULT 0,
    "commission_rate" INT NOT NULL DEFAULT 0,
    "admission_application_id" INT NOT NULL UNIQUE REFERENCES "agentadmissionapplication" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "agentadmissionapplication" DROP COLUMN "status";
        DROP TABLE IF EXISTS "agentapplicationcommission";"""
