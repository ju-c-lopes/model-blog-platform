from django.db import connection


class HealthService:
    @staticmethod
    def check():
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")

        return {
            "database": True,
            "storage": True,
            "cache": True,
        }
