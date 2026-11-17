
import streamlit as st
from pathlib import Path
import sys

# ==================================================
# 1. PROJECT CONFIGURATION
# ==================================================

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from config.settings import UPLOAD_DIR
from ingestion.indexer import build_vectorstore
from agents.research_agent import run_research_agent


# ==================================================
# 2. PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="REGE | AI Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================================================
# 3. CUSTOM CSS
# ==================================================

st.markdown("""
<style>

/* Main application background */
.stApp {
    background: linear-gradient(135deg, #0b1020 0%, #11182b 55%, #15112b 100%);
    color: #f1f5f9;
}

/* Main content width and spacing */
.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111a30 0%, #17142d 100%);
    border-right: 1px solid rgba(148, 163, 184, 0.15);
}

section[data-testid="stSidebar"] > div {
    padding-top: 2rem;
}

/* Typography */
h1, h2, h3 {
    color: #f8fafc !important;
    letter-spacing: -0.5px;
}

p, label, .stMarkdown {
    color: #cbd5e1;
}

/* Hero section */
.hero {
    padding: 30px;
    border-radius: 22px;
    background: linear-gradient(
        120deg,
        rgba(79, 70, 229, 0.30),
        rgba(124, 58, 237, 0.18),
        rgba(14, 165, 233, 0.12)
    );
    border: 1px solid rgba(139, 92, 246, 0.35);
    margin-bottom: 28px;
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.18);
}

.hero-tag {
    color: #c4b5fd;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
}

.hero-title {
    color: #ffffff;
    font-size: 34px;
    font-weight: 800;
    margin-top: 10px;
    line-height: 1.25;
}

.hero-description {
    color: #cbd5e1;
    font-size: 15px;
    margin-top: 10px;
}

/* Dashboard cards */
.panel {
    background: rgba(30, 41, 59, 0.72);
    border: 1px solid rgba(148, 163, 184, 0.16);
    border-radius: 18px;
    padding: 20px;
    margin-bottom: 16px;
}

.panel-title {
    color: #f8fafc;
    font-size: 17px;
    font-weight: 700;
    margin-bottom: 7px;
}

.panel-description {
    color: #94a3b8;
    font-size: 13px;
}

/* Status badges */
.status {
    display: inline-block;
    padding: 6px 11px;
    border-radius: 30px;
    font-size: 11px;
    font-weight: 700;
    background: rgba(16, 185, 129, 0.13);
    color: #6ee7b7;
    border: 1px solid rgba(16, 185, 129, 0.25);
}

/* Buttons */
.stButton > button {
    border-radius: 10px;
    border: 1px solid rgba(139, 92, 246, 0.35);
    background: linear-gradient(100deg, #6366f1, #8b5cf6);
    color: white;
    font-weight: 650;
    padding: 10px 16px;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    border-color: #c4b5fd;
    background: linear-gradient(100deg, #4f46e5, #7c3aed);
    transform: translateY(-1px);
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: rgba(15, 23, 42, 0.55);
    border: 1px dashed rgba(139, 92, 246, 0.55);
    border-radius: 13px;
    padding: 10px;
}

/* Text input and chat input */
.stTextArea textarea,
.stTextInput input,
[data-testid="stChatInput"] textarea {
    background: #172238 !important;
    color: #f8fafc !important;
    border: 1px solid #334155 !important;
    border-radius: 12px !important;
}

/* Chat messages */
[data-testid="stChatMessage"] {
    background: rgba(30, 41, 59, 0.65);
    border: 1px solid rgba(148, 163, 184, 0.12);
    border-radius: 16px;
    padding: 15px;
    margin-bottom: 13px;
}

/* Dividers */
hr {
    border-color: rgba(148, 163, 184, 0.15);
}

/* Footer */
.footer {
    text-align: center;
    color: #64748b;
    font-size: 12px;
    padding: 25px 0 5px;
}

/* Small screens */
@media (max-width: 768px) {
    .hero {
        padding: 20px;
    }

    .hero-title {
        font-size: 25px;
    }

    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }
}

</style>
""", unsafe_allow_html=True)


# ==================================================
# 4. SESSION STATE
# ==================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "index_ready" not in st.session_state:
    st.session_state.index_ready = False


# ==================================================
# 5. SIDEBAR - DOCUMENT MANAGEMENT
# ==================================================

with st.sidebar:

    st.markdown("""
    <div style="padding-bottom:20px;">
        <div style="font-size:27px;font-weight:800;color:white;">
            🔬 REGE
        </div>
        <div style="font-size:12px;color:#94a3b8;letter-spacing:1px;">
            INTELLIGENT RESEARCH SYSTEM
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("### 📁 Knowledge Center")
    st.caption("Upload documents to build your research knowledge base.")

    uploaded_files = st.file_uploader(
        "Choose your documents",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
        help="Supported formats: PDF, DOCX and TXT"
    )

    if st.button("⬆ Save Documents", use_container_width=True):

        if uploaded_files:

            saved_count = 0

            for uploaded_file in uploaded_files:

                file_name = Path(uploaded_file.name).name
                file_path = UPLOAD_DIR / file_name

                with open(file_path, "wb") as file:
                    file.write(uploaded_file.getbuffer())

                saved_count += 1

            st.success(f"{saved_count} document(s) saved!")
            st.session_state.index_ready = False

        else:
            st.warning("Please select documents first.")

    st.divider()

    # List saved documents
    st.markdown("### 📚 Saved Documents")

    saved_documents = [
        file for file in UPLOAD_DIR.iterdir()
        if file.is_file()
        and file.suffix.lower() in [".pdf", ".docx", ".txt"]
    ]

    st.caption(f"{len(saved_documents)} document(s) available")

    if saved_documents:

        for document in saved_documents:

            st.markdown(
                f"""
                <div style="
                    background:rgba(30,41,59,0.7);
                    border:1px solid rgba(148,163,184,0.13);
                    padding:10px;
                    border-radius:10px;
                    margin-bottom:7px;
                    font-size:12px;
                    color:#cbd5e1;
                    word-break:break-word;
                ">
                    📄 {document.name}
                </div>
                """,
                unsafe_allow_html=True
            )

    else:
        st.caption("No documents uploaded yet.")

    st.divider()

    # Indexing section
    st.markdown("### 🧠 Knowledge Base")

    st.caption(
        "Convert your documents into searchable vector embeddings."
    )

    if st.button("⚡ Build FAISS Index", use_container_width=True):

        if saved_documents:

            try:

                with st.spinner("Building your knowledge base..."):

                    build_vectorstore(UPLOAD_DIR)

                st.session_state.index_ready = True
                st.success("Knowledge base created successfully!")

            except Exception as error:
                st.error(f"Indexing failed: {error}")

        else:
            st.warning("Save documents before indexing.")

    if st.session_state.index_ready:
        st.markdown(
            '<span class="status">● Knowledge Base Ready</span>',
            unsafe_allow_html=True
        )

    st.divider()

    st.markdown("""
    <div style="font-size:12px;color:#94a3b8;line-height:2;">
        <b style="color:#c4b5fd;">TECHNOLOGY STACK</b><br>
        🦙 Ollama & Llama 3.2<br>
        🔗 LangChain<br>
        🗄️ FAISS Vector Database<br>
        🌐 Tavily Search<br>
        ⚡ Streamlit
    </div>
    """, unsafe_allow_html=True)


# ==================================================
# 6. MAIN HERO SECTION
# ==================================================

st.markdown("""
<div class="hero">
    <div class="hero-tag">AI POWERED KNOWLEDGE DISCOVERY</div>

    <div class="hero-title">
        Multi-Source AI Research Agent
    </div>

    <div class="hero-description">
        Explore your documents, discover information from the web,
        and generate intelligent research answers in one place.
    </div>
</div>
""", unsafe_allow_html=True)


# ==================================================
# 7. DASHBOARD OVERVIEW
# ==================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="panel">
        <div class="panel-title">📄 Document Search</div>
        <div class="panel-description">
            Retrieve information from your uploaded documents.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="panel">
        <div class="panel-title">🌐 Web Intelligence</div>
        <div class="panel-description">
            Discover external information using Tavily search.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="panel">
        <div class="panel-title">🧠 AI Research</div>
        <div class="panel-description">
            Combine multiple sources into meaningful answers.
        </div>
    </div>
    """, unsafe_allow_html=True)


# ==================================================
# 8. RESEARCH CHAT INTERFACE
# ==================================================

st.markdown("## 💬 Research Workspace")

st.caption(
    "Ask questions about your uploaded documents or explore topics on the internet."
)

# Display conversation history
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# User chat input
question = st.chat_input(
    "Ask anything... e.g. Compare my PDF with recent AI developments."
)


# ==================================================
# 9. RESEARCH AGENT EXECUTION
# ==================================================

if question:

    # Store and display user question
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user"):
        st.markdown(question)

    # Generate response
    with st.chat_message("assistant"):

        with st.spinner("🔍 Researching across available sources..."):

            try:

                answer = run_research_agent(question)

                st.markdown(answer)

                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )

            except Exception as error:

                error_message = f"Research failed: {error}"

                st.error(error_message)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_message
                    }
                )


# ==================================================
# 10. FOOTER
# ==================================================

st.divider()

st.markdown("""
<div class="footer">
    REGE — Multi-Source AI Research Agent<br>
    Built with Python • LangChain • Ollama • FAISS • Tavily • Streamlit
</div>
""", unsafe_allow_html=True)
