import logging
from snowflake.connector import connect
from dotenv import load_dotenv
import os
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def query_police_events(query="SELECT * FROM EXAM_DB.MART.MART_EVENTS"):
    load_dotenv()

    try:
        with connect(
            user=os.getenv("SNOWFLAKE_USER"),
            password=os.getenv("SNOWFLAKE_PASSWORD"),
            account=os.getenv("SNOWFLAKE_ACCOUNT"),
            warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
            database=os.getenv("SNOWFLAKE_DATABASE"),
            schema=os.getenv("SNOWFLAKE_SCHEMA"),
            role=os.getenv("SNOWFLAKE_ROLE"),
            login_timeout=60,  # Increase login timeout
            network_timeout=60  # Increase network timeout
        ) as conn:
            logger.info("Successfully connected to Snowflake")
            conn.cursor().execute(f"USE WAREHOUSE {os.getenv('SNOWFLAKE_WAREHOUSE')}")
            df = pd.read_sql(query, conn)
            logger.info("Fetched data from Snowflake: %s", df.head())
        return df
    except Exception as e:
        logger.error("Failed to connect to Snowflake", exc_info=True)
        raise