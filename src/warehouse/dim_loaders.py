import pandas as pd
from warehouse.loader import WarehouseLoader

loader = WarehouseLoader()
conn = loader.get_connection()

def load_dim_staff():
    
    # file_path = loader.download_parquet(bucket, key)
    # df = pd.read_parquet(file_path)

    sql = """
        INSERT INTO dim_staff (
            staff_id,
            first_name,
            last_name,
            department,
            email
        )
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (staff_id) DO NOTHING;
    """

    records = df[[
        "staff_id",
        "first_name",
        "last_name",
        "department",
        "email"
    ]].values.tolist()

    for record in records:
        conn.run(sql, record)

    loader.close()
