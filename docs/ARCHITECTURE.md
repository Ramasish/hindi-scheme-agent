# Architecture Document

## System Design
The system follows a **Voice-First Agentic Workflow** utilizing the **ReAct (Reason + Act)** pattern.

### 1. High-Level Data Flow
```mermaid
graph TD
    User((User)) -- "Voice (Hindi)" --> STT[Speech-to-Text]
    STT -- "Text (Hindi)" --> Brain[LLM Agent / Planner]
    
    subgraph "Agent Core"
        Brain -- "Reasoning" --> Router{Decision}
        Router -- "Need Data?" --> Tools[Tool Execution]
        Router -- "Reply?" --> Generator[Response Generator]
        Tools -- "JSON Result" --> Brain
    end
    
    Generator -- "Text (Hindi)" --> TTS[Text-to-Speech]
    TTS -- "Audio" --> User