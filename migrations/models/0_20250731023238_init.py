from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "user" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "username" VARCHAR(50) NOT NULL UNIQUE,
    "email" VARCHAR(100) NOT NULL UNIQUE,
    "password_hash" VARCHAR(128) NOT NULL,
    "is_admin" INT NOT NULL DEFAULT 0,
    "is_verified" INT NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS "userprofile" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "full_name" VARCHAR(100) NOT NULL,
    "phone" VARCHAR(25) NOT NULL,
    "whatsapp" VARCHAR(25) NOT NULL,
    "address" VARCHAR(500) NOT NULL,
    "occupation" VARCHAR(255) NOT NULL,
    "experience" INT NOT NULL DEFAULT 0,
    "exp_description" TEXT,
    "initial_refffer" VARCHAR(255) NOT NULL,
    "no_of_deal" INT NOT NULL DEFAULT 0,
    "office" INT NOT NULL DEFAULT 0,
    "office_address" VARCHAR(255),
    "student_country" VARCHAR(100) NOT NULL,
    "student_destination_country" VARCHAR(100) NOT NULL,
    "special_service" TEXT,
    "nid_passport_file" VARCHAR(500),
    "user_id" INT NOT NULL UNIQUE REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "country" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "name" VARCHAR(100) NOT NULL,
    "description" TEXT
);
CREATE TABLE IF NOT EXISTS "university" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "varsity_type" VARCHAR(11) NOT NULL DEFAULT 'Public' /* PUBLIC: Public\nPRIVATE: Private\nSEMI_PUBLIC: Semi Public */,
    "name" VARCHAR(300) NOT NULL,
    "location" VARCHAR(300) NOT NULL,
    "description" TEXT,
    "image" VARCHAR(255),
    "country_id" INT NOT NULL REFERENCES "country" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "course" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "name" VARCHAR(200) NOT NULL,
    "course_type" VARCHAR(200),
    "fee" INT,
    "image" VARCHAR(255),
    "university_id" INT NOT NULL REFERENCES "university" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "agentadmissionapplication" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "first_name" VARCHAR(55) NOT NULL,
    "last_name" VARCHAR(55) NOT NULL,
    "email" VARCHAR(55) NOT NULL,
    "phone" VARCHAR(20) NOT NULL,
    "passport_no" VARCHAR(100) NOT NULL,
    "last_graduation" VARCHAR(55),
    "status" VARCHAR(21) NOT NULL DEFAULT 'New' /* NEW: New\nREVIEW: Review\nCOMMISSION_PAID: Commission Paid\nREJECTED: Rejected\nCONDITIONALOFFER: Conditional Offer\nUNCONDITIONALOFFER: Unconditional Offer\nCASDOCUMENTPENDING: CAS Documents Pending\nCASINTERVIEWPENDING: CAS InterView Pending\nCASINTERVIEWPASSED: CAS InterView Passed\nCASRECEIVED: CAS Received\nAPPLYFORVISA: Apply For Visa\nVISARECEIVED: Visa Received\nENROLLEMENTPENDING: Enrollement Pending\nENROLLEMENTCOMPLETE: Enrollement Complete */,
    "agent_id" INT REFERENCES "user" ("id") ON DELETE SET NULL,
    "course_id" INT REFERENCES "course" ("id") ON DELETE SET NULL,
    "university_one_id" INT REFERENCES "university" ("id") ON DELETE SET NULL,
    "university_three_id" INT REFERENCES "university" ("id") ON DELETE SET NULL,
    "university_two_id" INT REFERENCES "university" ("id") ON DELETE SET NULL
);
CREATE TABLE IF NOT EXISTS "agentapplicationcommission" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "student_fee" INT NOT NULL DEFAULT 0,
    "commission" INT NOT NULL DEFAULT 0,
    "commission_rate" INT NOT NULL DEFAULT 0,
    "admission_application_id" INT NOT NULL UNIQUE REFERENCES "agentadmissionapplication" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "agentapplicationdocuments" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "passport" VARCHAR(300),
    "masters_certificate" VARCHAR(300),
    "masters_transcript" VARCHAR(300),
    "honers_certificate" VARCHAR(300),
    "honers_transcript" VARCHAR(300),
    "hsc_certificate" VARCHAR(300),
    "hsc_transcript" VARCHAR(300),
    "ssc_certificate" VARCHAR(300),
    "ssc_transcript" VARCHAR(300),
    "ielts_certificate" VARCHAR(300),
    "cv" VARCHAR(300),
    "resume" VARCHAR(300),
    "lor" VARCHAR(300),
    "job_letter" VARCHAR(300),
    "others" VARCHAR(300),
    "admission_application_id" INT NOT NULL UNIQUE REFERENCES "agentadmissionapplication" ("id") ON DELETE CASCADE
);
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
    "current_stage" VARCHAR(200),
    "preferred_university_id" INT NOT NULL REFERENCES "university" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "studentapplicationdocuments" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "passport" VARCHAR(300),
    "last_graduation_certificate" VARCHAR(300),
    "admission_application_id" INT NOT NULL UNIQUE REFERENCES "studentadmissionapplication" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
