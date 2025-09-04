from upload_sql_records import ingest_all_records

def update_all_records_created_in_last_week():
    sql_query = (
        "SELECT * FROM Products WHERE `Date Modified` >= DATEADD(day, -7, GETDATE())"
    )

    ingest_all_records(sql_query)