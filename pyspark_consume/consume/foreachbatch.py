from .config import settings


def foreach_batch_function(df, epoch_id):
    df.select("*").write.format("jdbc")\
        .mode("append")\
        .option("url", f"jdbc:postgresql://{settings.database_hostname}:{settings.database_port}/{settings.database_name}") \
        .option("driver", "org.postgresql.Driver").option("dbtable", "environment_readings") \
        .option("user", settings.database_username).option("password", settings.database_password).save()
    pass
