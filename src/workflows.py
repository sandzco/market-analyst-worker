from datetime import timedelta
from temporalio import workflow

@workflow.defn
class StockAnalysisWorkflow:
    @workflow.run
    async def run(self, ticker: str) -> str:
        # STEP 1: Get Hard Data (Deterministic)
        market_data = await workflow.execute_activity(
            "get_stock_data",
            args=[ticker],
            start_to_close_timeout=timedelta(seconds=15)
        )

        # STEP 2: Analyze with AI (Probabilistic)
        analysis_prompt = (
            f"Here is the real-time market data for {ticker}:\n\n"
            f"{market_data}\n\n"
            f"Based on this data, write a brief 3-sentence technical analysis "
            f"of the trend. Is it bullish or bearish?"
        )

        final_insight = await workflow.execute_activity(
            "call_ai_model",
            args=[analysis_prompt, "You are a senior technical analyst."],
            start_to_close_timeout=timedelta(seconds=600)
        )
        
        # Return both for debugging transparency
        return f"--- 📊 RAW DATA ---\n{market_data}\n\n--- 🧠 AI INSIGHT ---\n{final_insight}"