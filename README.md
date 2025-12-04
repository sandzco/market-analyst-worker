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
