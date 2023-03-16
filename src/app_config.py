from os import environ as env

flask_config = {
    "PORT": int(env.get("PORT", 4000)),
    "DEBUG_MODE": int(env.get("DEBUG_MODE", 1)),
    "HOST": str(env.get("HOST", "0.0.0.0")),
    "timeout": int(env.get("TIMEOUT", 5000))
}
