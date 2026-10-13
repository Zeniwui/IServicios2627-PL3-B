# Definición de secretos a usar por la app
import os
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "sqlite://")

# # Definición de secretos a usar por la app
# SQLALCHEMY_DATABASE_URI = "mysql+pymysql://amigosuser:amigospass@172.18.0.2/amigosdb"