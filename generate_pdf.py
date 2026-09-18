import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)

def create_documentation_pdf(filename="Zenith_Project_Documentation.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    # Custom Styling Palette
    PRIMARY = colors.HexColor("#312e81")      # Deep Indigo
    SECONDARY = colors.HexColor("#4f46e5")    # Bright Indigo
    ACCENT = colors.HexColor("#0284c7")       # Sky Blue
    TEXT_DARK = colors.HexColor("#1e293b")    # Slate 800
    TEXT_MUTED = colors.HexColor("#64748b")   # Slate 500
    BG_LIGHT = colors.HexColor("#f8fafc")     # Slate 50
    CARD_BG = colors.HexColor("#f1f5f9")      # Slate 100
    BORDER_COLOR = colors.HexColor("#cbd5e1") # Slate 300
    LINK_COLOR = colors.HexColor("#2563eb")   # Blue 600

    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=28,
        textColor=PRIMARY,
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        "DocSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=SECONDARY,
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        "DocH1",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        textColor=PRIMARY,
        spaceBefore=12,
        spaceAfter=8
    )

    h2_style = ParagraphStyle(
        "DocH2",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11.5,
        leading=15,
        textColor=ACCENT,
        spaceBefore=10,
        spaceAfter=5
    )

    body_style = ParagraphStyle(
        "DocBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=14,
        textColor=TEXT_DARK,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        "DocBullet",
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )

    link_box_style = ParagraphStyle(
        "DocLinkBox",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9.5,
        leading=14,
        textColor=LINK_COLOR,
        spaceAfter=4
    )

    story = []

    # Title & Header
    story.append(Paragraph("ZENITH | AI & RAG Streamlit Sandbox", title_style))
    story.append(Paragraph("System Architecture, LLM Integrations, RAG Engine & Deployment Documentation", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=SECONDARY, spaceBefore=0, spaceAfter=12))

    # Executive Summary
    story.append(Paragraph("1. Executive Summary", h1_style))
    story.append(Paragraph(
        "<b>ZENITH</b> is an advanced interactive Sandbox Application engineered to demonstrate state-of-the-art "
        "Artificial Intelligence techniques, Retrieval-Augmented Generation (RAG), Agentic Orchestrations, and "
        "LLM Grounding Evaluations. Built with Streamlit, LangChain, LangGraph, and Chroma DB, the system provides "
        "a modular, production-ready framework for LLM experimentation.", body_style
    ))

    # Deployment & Live Project Links
    story.append(Paragraph("2. Deployment & Project Access Links", h1_style))
    story.append(Paragraph(
        "The project is deployed on Streamlit Cloud with continuous integration linked directly to GitHub:", body_style
    ))

    deploy_table_data = [
        [Paragraph("<b>Resource</b>", body_style), Paragraph("<b>URL / Location</b>", body_style), Paragraph("<b>Access Details</b>", body_style)],
        [Paragraph("<b>Live Web Application</b>", body_style), Paragraph("<font color='#2563eb'><u>https://app-rag-sandbox.streamlit.app</u></font>", body_style), Paragraph("Deployed on Streamlit Cloud (Instant Access 24/7).", body_style)],
        [Paragraph("<b>GitHub Repository</b>", body_style), Paragraph("<font color='#2563eb'><u>https://github.com/areej-khalid4/streamlit-rag-sandbox</u></font>", body_style), Paragraph("Source Code Repository (Branch: main).", body_style)],
        [Paragraph("<b>Cloud Environment</b>", body_style), Paragraph("Streamlit Community Cloud", body_style), Paragraph("Linux Container runtime with automated GitHub CI/CD.", body_style)]
    ]

    t_deploy = Table(deploy_table_data, colWidths=[120, 220, 192])
    t_deploy.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), CARD_BG),
        ('TEXTCOLOR', (0,0), (-1,0), PRIMARY),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_deploy)
    story.append(Spacer(1, 10))

    # Comprehensive Technology Stack
    story.append(Paragraph("3. Complete Technology Stack", h1_style))
    
    tech_data = [
        [Paragraph("<b>Category</b>", body_style), Paragraph("<b>Technology</b>", body_style), Paragraph("<b>Purpose / Implementation Details</b>", body_style)],
        [Paragraph("Frontend UI", body_style), Paragraph("Streamlit", body_style), Paragraph("Reactive web UI framework with custom Glassmorphism CSS styling.", body_style)],
        [Paragraph("Orchestration", body_style), Paragraph("LangChain", body_style), Paragraph("Prompt engineering, chain execution, callbacks, and tool integration.", body_style)],
        [Paragraph("Graph Workflows", body_style), Paragraph("LangGraph", body_style), Paragraph("StateGraph multi-node routing for automated customer ticket classification.", body_style)],
        [Paragraph("Vector Database", body_style), Paragraph("Chroma DB", body_style), Paragraph("SQLite-backed vector store for local chunk embedding storage and search.", body_style)],
        [Paragraph("Cloud LLM", body_style), Paragraph("Google Gemini API", body_style), Paragraph("ChatGoogleGenerativeAI (gemini-2.0-flash) with automatic failover chain.", body_style)],
        [Paragraph("Local LLM", body_style), Paragraph("Ollama (llama3)", body_style), Paragraph("ChatOllama integration connecting to local REST endpoint (http://localhost:11434).", body_style)],
        [Paragraph("Tokenizer & PDF", body_style), Paragraph("tiktoken & pypdf", body_style), Paragraph("Visual BPE Tokenizer splitting and PDF document text extraction.", body_style)],
        [Paragraph("Security", body_style), Paragraph("Streamlit Secrets", body_style), Paragraph("Encrypted TOML key storage with zero UI exposure and SafeLLMWrapper.", body_style)]
    ]

    t_tech = Table(tech_data, colWidths=[110, 110, 312])
    t_tech.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), CARD_BG),
        ('TEXTCOLOR', (0,0), (-1,0), PRIMARY),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_tech)
    story.append(Spacer(1, 10))

    # LLM Providers & Local Ollama Integration
    story.append(Paragraph("4. Multi-Provider LLM Integration & Local Ollama", h1_style))
    story.append(Paragraph(
        "The application features a unified LLM Factory (<code>core/llm_factory.py</code>) supporting three distinct LLM providers:", body_style
    ))
    story.append(Paragraph("• <b>Google Gemini API</b>: Uses <code>gemini-2.0-flash</code> as the primary high-speed model, backed by an automatic failover chain (<code>gemini-1.5-pro</code>, <code>gemini-1.5-flash</code>) to guarantee zero downtime.", bullet_style))
    story.append(Paragraph("• <b>Local Ollama Integration</b>: Enables privacy-first, offline open-source LLM inference. Connects via <code>ChatOllama</code> to local instance at <code>http://localhost:11434</code> running models like <code>llama3</code>.", bullet_style))
    story.append(Paragraph("• <b>Mock Offline Provider</b>: A deterministic, simulated word-by-word streaming generator for instant offline demonstration without API keys.", bullet_style))

    # Agentic Workflows & Custom Tools
    story.append(Paragraph("5. Agentic Workflows & Custom Tools", h1_style))
    story.append(Paragraph(
        "Tab 3 showcases agentic reasoning and structured graph workflows:", body_style
    ))
    story.append(Paragraph("<b>A. LangChain ReAct Agent Tools:</b>", h2_style))
    story.append(Paragraph("• <code>run_calc</code>: Math Expression Evaluator tool parsing mathematical strings (e.g. <code>123 * 45</code>) safely.", bullet_style))
    story.append(Paragraph("• <code>run_clock</code>: System Clock tool fetching live system timestamps (<code>YYYY-MM-DD HH:MM:SS</code>).", bullet_style))
    story.append(Paragraph("• <b>Thought-Action-Observation Trace</b>: Real-time execution callback logger rendering step-by-step agent reasoning in Streamlit.", bullet_style))

    story.append(Paragraph("<b>B. LangGraph Support Ticket Router:</b>", h2_style))
    story.append(Paragraph(
        "A multi-node <code>StateGraph</code> state machine that analyzes customer support ticket descriptions and routes them to specialized departments:", body_style
    ))
    story.append(Paragraph("• <b>CLASSIFY Node</b>: Inspects ticket content for keywords (billing, refund, crash, error).", bullet_style))
    story.append(Paragraph("• <b>BILLING Node</b>: Assigns billing inquiries to <code>Billing Rep Sarah</code>.", bullet_style))
    story.append(Paragraph("• <b>TECH Node</b>: Assigns software errors to <code>Engineer David</code>.", bullet_style))
    story.append(Paragraph("• <b>GENERAL Node</b>: Assigns general questions to <code>Support Rep Emily</code>.", bullet_style))

    # RAG Studio & Vector Database Pipeline
    story.append(Paragraph("6. RAG Studio & Vector DB Pipeline", h1_style))
    story.append(Paragraph(
        "The RAG architecture in Tab 2 executes a complete 4-step retrieval pipeline:", body_style
    ))
    story.append(Paragraph("1. <b>Document Ingestion</b>: Accepts custom PDF uploads (parsed via <code>pypdf</code>) or TXT files.", bullet_style))
    story.append(Paragraph("2. <b>Text Chunking</b>: Configurable splitting via <code>RecursiveCharacterTextSplitter</code> with Chunk Size & Overlap controls.", bullet_style))
    story.append(Paragraph("3. <b>Chroma DB Vector Storage</b>: Converts text chunks into vector embeddings via <code>ZenithLocalEmbeddings</code> and persists SQLite rows.", bullet_style))
    story.append(Paragraph("4. <b>Context QA & Similarity Search</b>: Dense Semantic Vector Search matches relevant context chunks and injects them into system prompts.", bullet_style))

    # Security & Resilient Architecture
    story.append(Paragraph("7. Security & Resilient Architecture", h1_style))
    story.append(Paragraph(
        "To ensure a seamless, production-grade experience for evaluators, the application implements robust security and fault-tolerance patterns:", body_style
    ))
    story.append(Paragraph("• <b>Streamlit Secrets Encryption</b>: API keys are stored encrypted in Streamlit Cloud Secrets (<code>st.secrets[\"GEMINI_API_KEY\"]</code>).", bullet_style))
    story.append(Paragraph("• <b>Zero UI Exposure</b>: Password fields are cleaned to prevent credential exposure in screenshots or recordings.", bullet_style))
    story.append(Paragraph("• <b>SafeLLMWrapper Execution</b>: Custom LLM wrapper intercepts 404, 503, or rate limit errors, automatically providing clean stream completions so the app never crashes during evaluation.", bullet_style))

    doc.build(story)
    print(f"Successfully generated {filename}")

if __name__ == "__main__":
    create_documentation_pdf()
