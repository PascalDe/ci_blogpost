import mysql.connector
from typing import Optional
import logging
import time

logger = logging.getLogger(__name__)


def get_known_resolution(
    error_message: str,
    error_code: Optional[str] = None,
    system_sender: Optional[str] = None,
):
    logger.info("MariaDB query START")
    start = time.time()

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="[YOUR PASSWORD]", # <-- Enter password here!
        database="ciDB",
    )

    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT error_code, error_message, resolution
        FROM errorTable
        WHERE error_message LIKE %s
        ORDER BY created_at DESC
        LIMIT 1
    """

    cursor.execute(query, (f"%{error_message[:100]}%",))
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    logger.info(
        "MariaDB query END (%.3fs) – hit=%s",
        time.time() - start,
        bool(row),
    )

    return row
