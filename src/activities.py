import os
import yfinance as yf
from temporalio import activity
from langchain_community.llms import Ollama

# Configuration defaults to the K8s headless service
OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://inference-provider.ai-platform.svc.cluster.local:11434")

@activity.defn(name="get_stock_data")
async def get_stock_data(ticker: str) -> str:
    print(f"📉 Fetching market data for: {ticker}")
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="5d")
        if hist.empty:
            return f"Error: No data found for symbol {ticker}. It may be delisted."
        
        data_summary = f"Recent Market Data for {ticker}:\n"
        for date, row in hist.iterrows():
            data_summary += f"- {date.strftime('%Y-%m-%d')}: ${row['Close']:.2f}\n"
            
        return data_summary
    except Exception as e:
        return f"Error fetching data: {str(e)}"

@activity.defn(name="call_ai_model")
async def call_ai_model(prompt: str, system_role: str) -> str:
    print(f"🤖 Connecting to Brain at: {OLLAMA_URL}")
    try:
        llm = Ollama(
            base_url=OLLAMA_URL,
            model="llama3", 
            temperature=0.2
        )
        full_prompt = f"System: {system_role}\n\nUser: {prompt}"
        return llm.invoke(full_prompt)
    except Exception as e:
        return f"Error connecting to Inference Engine: {str(e)}"