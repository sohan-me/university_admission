# TORTOISE_ORM = {
#     "connections": {"default": "sqlite://db.sqlite3"},
#     "apps": {
#         "models": {
#             "models": ["users.models", "engine.models", "aerich.models"],
#             "default_connection": "default",
#         },
#     },
# }




TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",  # async driver - better performance
            "credentials": {
                "host": "localhost",   # or your actual DB host from cPanel
                "port": "5432",
                "user": "abrorsgb_user",
                "password": "abroad'Admission",  # avoid special chars or use env vars
                "database": "abrorsgb_db",
            }
        }
    },
    "apps": {
        "models": {
            "models": ["users.models", "engine.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}
