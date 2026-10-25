import csv
import io
import logging
import os
import uuid
from datetime import datetime, timezone

import azure.functions as func
from azure.storage.blob import BlobServiceClient

app = func.FunctionApp()


@app.timer_trigger(
    schedule="0 30 0 * * *",
    arg_name="timer",
    run_on_startup=False,
    use_monitor=True,
)
def daily_order_ingestion(timer: func.TimerRequest) -> None:
    """Generate synthetic retail orders and store them in Bronze."""
    if timer.past_due:
        logging.warning("The scheduled ingestion is running late.")

    connection_string = os.environ["AzureWebJobsStorage"]
    container_name = os.getenv("BRONZE_CONTAINER", "bronze")

    now = datetime.now(timezone.utc)
    batch_id = uuid.uuid4().hex[:8]

    output = io.StringIO()
    columns = [
        "order_id", "customer_id", "product_id", "category",
        "store_id", "order_date", "status", "quantity",
        "unit_price", "delivery_days", "promised_days", "ingested_at",
    ]

    writer = csv.DictWriter(output, fieldnames=columns)
    writer.writeheader()

    # Synthetic sample data for demonstrating ingestion.
    for i in range(100):
        writer.writerow({
            "order_id": f"{batch_id}-{i + 1}",
            "customer_id": f"CUST-{i % 40 + 1:03d}",
            "product_id": f"PROD-{i % 7 + 1:03d}",
            "category": ["Electronics", "Home", "Fashion", "Grocery",
                         "Beauty", "Sports", "Books"][i % 7],
            "store_id": f"STORE-{i % 5 + 1:02d}",
            "order_date": now.date().isoformat(),
            "status": ["Delivered", "Shipped", "Cancelled"][i % 3],
            "quantity": i % 4 + 1,
            "unit_price": round(100 + (i % 20) * 25.5, 2),
            "delivery_days": i % 7 + 1,
            "promised_days": 4,
            "ingested_at": now.isoformat(),
        })

    blob_service = BlobServiceClient.from_connection_string(
        connection_string
    )
    blob_name = (
        f"incremental/orders_{now.strftime('%Y%m%dT%H%M%S')}_"
        f"{batch_id}.csv"
    )

    blob_service.get_blob_client(
        container=container_name,
        blob=blob_name,
    ).upload_blob(output.getvalue(), overwrite=False)

    logging.info("Uploaded synthetic order batch: %s", blob_name)
