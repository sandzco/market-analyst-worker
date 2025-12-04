import asyncio
import os
from temporalio.client import Client
from temporalio.worker import Worker

# Import components
from workflows import StockAnalysisWorkflow
from activities import call_ai_model, get_stock_data

# Configuration
TEMPORAL_HOST = os.getenv("TEMPORAL_HOST", "temporal-stack-frontend.default.svc.cluster.local:7233")
TASK_QUEUE = os.getenv("TEMPORAL_TASK_QUEUE", "finance-analytics-v1")

async def main():
    print(f"🔌 Connecting to Temporal at: {TEMPORAL_HOST}")
    client = await Client.connect(TEMPORAL_HOST)

    worker = Worker(
        client,
        task_queue=TASK_QUEUE,
        workflows=[StockAnalysisWorkflow],
        activities=[call_ai_model, get_stock_data],
    )

    print(f"Smart Worker started on queue: {TASK_QUEUE}")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())