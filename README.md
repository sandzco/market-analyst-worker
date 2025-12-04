# 📈 Distributed AI Market Analyst

A hybrid-cloud AI Agent platform built on **Kubernetes** and **Temporal**.

This project demonstrates a production-grade architecture for "Agentic AI." Instead of a simple chatbot, it uses a distributed workflow engine to orchestrate deterministic tools (fetching real-time stock data) with probabilistic inference (LLMs running on a dedicated GPU node).

## 🏗️ Architecture

- **Orchestrator:** Temporal.io (Self-hosted on Microk8s)
- **Compute:** Python Workers (Containerized in K8s)
- **Inference:** Ollama (Running on external Windows GPU)
- **Tools:** yFinance (Real-time market data)
- **Connectivity:** Headless Services (Routing K8s traffic to local LAN)

## ✨ Capabilities

1.  **Fault Tolerance:** If the Agent crashes or the API fails, Temporal automatically retries.
2.  **Hybrid Inference:** Offloads heavy LLM computation to a dedicated Gaming PC (Nvidia GPU) while keeping logic in the Cluster.
3.  **Real-Time Data:** Fetches live stock history to ground the AI's analysis in reality.
4.  **Sandboxed Workflows:** Strictly separates Workflow logic from Activity execution for reliability.

## 🚀 Installation

### 1. Prerequisites
- **Microk8s** (or any K8s cluster)
- **Ollama** running on a machine with a GPU (Port 11434 exposed)
- **Python 3.11+**

### 2. Infrastructure Setup
**Deploy Temporal to K8s:**
```bash
microk8s helm3 install temporal-stack temporal/temporal \
    --set elasticsearch.enabled=false \
    --set cassandra.enabled=false \
    --set postgresql.enabled=true
```

### Configure Networking: Edit k8s/external-gpu-service.yaml and add your GPU machine's static IP.

kubectl apply -f k8s/external-gpu-service.yaml

### 3. Deploy the Agent

```
docker build -t <DOCKERHUB_ID>/agent-worker:v5 ./src

docker push <DOCKERHUB_ID>/agent-worker:v5
```

### Deploy
```
kubectl apply -f k8s/agent-deployment.yaml
```

## 🎮 Usage

### 1. Open Communication Channel

Tunnel the Temporal Frontend port from the cluster to your local machine:
Bash

kubectl port-forward svc/temporal-stack-frontend 7233:7233

### 2. Run the Client

Execute the client script to send a stock ticker to the cluster.
Bash
```
# Install dependencies
pip install temporalio

# Run the trigger
python src/client.py
```
### 3. Expected Output

The system will:

1. Ingest the Ticker (e.g., "TSLA").

2. Worker fetches last 5 days of price data via yfinance.

3. Worker sends data + prompt to your Local GPU via Ollama.

4. AI analyzes the trend and returns a summary.

```📉 Fetching market data for: TSLA
(market-analyst-worker) C:\Users\sK\market-analyst-worker>python src\client.py
🔌 Connecting to Temporal at 192.168.1.12:7233...
🚀 Sending Stock Analysis Task for: 'TSLA'
✅ Workflow started! ID: stock-check-TSLA-01
⏳ Waiting for result...

==============================
📉 MARKET ANALYSIS FOR TSLA:
==============================
--- DEBUG: RAW TOOL DATA ---
Recent Market Data for TSLA:
- 2025-11-26: $426.58
- 2025-11-28: $430.17
- 2025-12-01: $430.14
- 2025-12-02: $429.24
- 2025-12-03: $446.74


--- AI INSIGHT ---
Based on the recent market data for TSLA, it appears that the stock 
has been trending upward with a strong bullish momentum, as evidenced 
by the consecutive higher highs and lows from November 28th to December 
3rd. This uptrend is likely driven by increasing investor confidence 
in Tesla's growth prospects and its expanding electric vehicle offerings. 
The recent price action suggests that TSLA may continue to push higher 
in the near term, potentially targeting new all-time highs.
==============================
```

## 🛠️ Troubleshooting

- "Connection Refused" on Agent: Ensure the inference-provider Endpoints yaml has the correct IP of your GPU machine.

- Windows Firewall: If Ollama is unreachable, run this in PowerShell Admin: New-NetFirewallRule -DisplayName "Ollama" -Direction Inbound -LocalPort 11434 -Protocol TCP -Action Allow
- Temporal Sandbox Error: Ensure langchain imports are ONLY in activities.py and never in workflows.py.

## 🛡️ License

MIT