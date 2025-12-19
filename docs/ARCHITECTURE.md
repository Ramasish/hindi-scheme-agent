# 🏗️ System Architecture: Seva (Hindi AI Agent)

## 1. Executive Summary
**Seva** is a voice-first, agentic AI system designed to assist users in identifying and applying for government welfare schemes. Unlike rigid state-machine chatbots, Seva utilizes a **Planner-Executor-Evaluator** architecture (ReAct Pattern). It autonomously perceives user intent, reasons about missing data, executes deterministic tools for validation, and synthesizes natural language responses in Hindi.

---

## 2. Agent Lifecycle & Decision Flow

The agent operates on an event-driven loop that processes audio input into actionable intelligence.

### High-Level Data Flow



```mermaid
graph TD
    User((User)) -- "Voice (Hindi)" --> STT[Speech Recognition Service]
    STT -- "Raw Text" --> Memory[Conversation Memory]
    Memory -- "Context + History" --> Planner["LLM Brain (Llama-3)"]
    
    subgraph "Reasoning Core"
        Planner -- "Analyze State" --> Router{Decision Point}
        Router -- "Missing Info?" --> Ask[Generate Follow-up Question]
        Router -- "Have Info?" --> ToolTrigger[Construct Tool Call]
    end
    
    ToolTrigger -- "JSON Args" --> Executor[Tool Execution Engine]
    
    subgraph "Tools Layer"
        Executor --> Eligibility[Eligibility Calculator]
        Executor --> DB[Scheme Database]
        Executor --> Application[Application Portal]
    end
    
    Eligibility -- "Status/Result" --> Planner
    Ask -- "Text Response" --> Synthesizer[Text-to-Speech]


    Planner -- "Final Answer" --> Synthesizer
    Synthesizer -- "Audio" --> User

