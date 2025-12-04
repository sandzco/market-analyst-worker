import asyncio
from temporalio.client import Client

# Ensure you port-forward before running: 
# kubectl port-forward svc/temporal-stack-frontend 7233:7233
TEMPORAL_HOST = "localhost:7233" # -- change to microk8s host ip
TASK_QUEUE = "finance-analytics-v1"

async def main():
    print(f"🔌 Connecting to Temporal at {TEMPORAL_HOST}...")
    client = await Client.connect(TEMPORAL_HOST)

    ticker = "TSLA" 
    print(f"🚀 Sending Stock Analysis Task for: '{ticker}'")

    handle = await client.start_workflow(
        "StockAnalysisWorkflow",
        ticker,
        id=f"analysis-{ticker}-001",
        task_queue=TASK_QUEUE,
    )

    print(f"✅ Workflow started! ID: {handle.id}")
    print("⏳ Waiting for result...")
    
    result = await handle.result()
    print("\n" + result)

if __name__ == "__main__":
    asyncio.run(main())