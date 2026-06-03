# app.py
# Streamlit UI for Multi-Agent Research Assistant

import streamlit as st
import importlib
import os
from dotenv import load_dotenv

load_dotenv()

# ── Page Configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Multi-Agent Research Assistant",
    page_icon="🤖",
    layout="wide"
)

# ── Title Section ─────────────────────────────────────────────────────────────
st.title("🤖 Multi-Agent Research Assistant")
st.markdown("Powered by **Groq + Llama 3.1** | 4 AI Agents working together")
st.divider()

# ── How it works section ──────────────────────────────────────────────────────
with st.expander("ℹ️ How it works"):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.info("📋 **Coordinator Agent**\nManages all agents and delegates tasks")
    with col2:
        st.info("🔍 **Research Agent**\nCollects detailed information on your topic")
    with col3:
        st.info("✂️ **Summarizer Agent**\nRemoves redundancy and creates clean summary")
    with col4:
        st.info("✅ **Reviewer Agent**\nChecks completeness and improves the summary")

st.divider()

# ── Input Section ─────────────────────────────────────────────────────────────
st.subheader("💬 Ask your question")
query = st.text_input(
    label="Enter your research topic:",
    placeholder="e.g. Explain Kubernetes architecture, What is machine learning...",
    label_visibility="collapsed"
)

run_button = st.button("🚀 Start Research", type="primary", use_container_width=True)

# ── Run agents when button clicked ───────────────────────────────────────────
if run_button:
    if not query.strip():
        st.warning("⚠️ Please type a question first!")
    else:
        st.divider()
        st.subheader("🔄 Agent Pipeline — Live Progress")

        # ── Import agents ─────────────────────────────────────────────────────
        research_module    = importlib.import_module("1_research_agent")
        summarizer_module  = importlib.import_module("2_summarizer_agent")
        reviewer_module    = importlib.import_module("3_reviewer_agent")
        coordinator_module = importlib.import_module("4_coordinator_agent")

        research_agent    = research_module.research_agent
        summarizer_agent  = summarizer_module.summarizer_agent
        reviewer_agent    = reviewer_module.reviewer_agent

        # ── import coordinator logger ─────────────────────────────────────────
        coordinator_logger = coordinator_module.logger

        # ── COORDINATOR: Initializing ─────────────────────────────────────────
        with st.status("📋 Coordinator Agent — Initializing pipeline...", expanded=True) as coordinator_status:
            st.write("📋 Coordinator: Received user query!")
            st.write(f"📋 Coordinator: Query = `{query}`")
            coordinator_logger.info(f"Coordinator started via Streamlit | Query: {query}")

            st.write("📋 Coordinator: Starting pipeline...")
            st.write("📋 Coordinator: Delegating to **Research Agent** first...")
            coordinator_status.update(
                label="📋 Coordinator Agent — Running pipeline...",
                state="running"
            )

            # ── STEP 1: Research Agent ────────────────────────────────────────
            with st.status("🔍 Research Agent — Collecting information...", expanded=True) as research_status:
                st.write("🔍 Research Agent: Starting research...")
                st.write("🔍 Research Agent: Sending query to Llama 3.1...")
                research_output = research_agent(query)
                st.write("🔍 Research Agent: Research complete! Sending back to Coordinator...")
                research_status.update(
                    label="✅ Research Agent — Done!",
                    state="complete"
                )

            coordinator_logger.info(f"STEP 1 complete | Research size: {len(research_output)} chars")
            st.write("📋 Coordinator: Received research output! ✅")
            st.write("📋 Coordinator: Delegating to **Summarizer Agent**...")

            with st.expander("📚 View Raw Research", expanded=False):
                st.markdown(research_output)

            # ── STEP 2: Summarizer Agent ──────────────────────────────────────
            with st.status("✂️ Summarizer Agent — Summarizing...", expanded=True) as summarizer_status:
                st.write("✂️ Summarizer Agent: Received research from Coordinator...")
                st.write("✂️ Summarizer Agent: Removing redundancy...")
                st.write("✂️ Summarizer Agent: Creating clean summary...")
                summary_output = summarizer_agent(research_output)
                st.write("✂️ Summarizer Agent: Summary complete! Sending back to Coordinator...")
                summarizer_status.update(
                    label="✅ Summarizer Agent — Done!",
                    state="complete"
                )

            coordinator_logger.info(f"STEP 2 complete | Summary size: {len(summary_output)} chars")
            st.write("📋 Coordinator: Received summary! ✅")
            st.write("📋 Coordinator: Delegating to **Reviewer Agent**...")

            with st.expander("📝 View Summary", expanded=False):
                st.markdown(summary_output)

            # ── STEP 3: Reviewer Agent ────────────────────────────────────────
            with st.status("✅ Reviewer Agent — Reviewing...", expanded=True) as reviewer_status:
                st.write("✅ Reviewer Agent: Received summary from Coordinator...")
                st.write("✅ Reviewer Agent: Checking for completeness...")
                st.write("✅ Reviewer Agent: Identifying missing information...")
                st.write("✅ Reviewer Agent: Improving the summary...")
                review_output = reviewer_agent(summary_output)
                st.write("✅ Reviewer Agent: Review complete! Sending back to Coordinator...")
                reviewer_status.update(
                    label="✅ Reviewer Agent — Done!",
                    state="complete"
                )

            coordinator_logger.info(f"STEP 3 complete | Review size: {len(review_output)} chars")
            st.write("📋 Coordinator: Received review! ✅")
            st.write("📋 Coordinator: All agents done! Compiling final report...")

            # ── Save Report ───────────────────────────────────────────────────
            final_report = f"""QUERY: {query}

=== RESEARCH (from Research Agent) ===
{research_output}

=== SUMMARY (from Summarizer Agent) ===
{summary_output}

=== REVIEWED & IMPROVED (from Reviewer Agent) ===
{review_output}
"""
            os.makedirs("outputs", exist_ok=True)
            filename = query[:30].replace(" ", "_").replace("/", "_") + ".txt"
            filepath = os.path.join("outputs", filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(final_report)

            coordinator_logger.info(f"Report saved to: {filepath}")
            coordinator_logger.info("Coordinator finished successfully via Streamlit!")

            st.write(f"📋 Coordinator: Report saved to `outputs/{filename}` ✅")
            st.write("📋 Coordinator: Pipeline complete! 🎉")

            # ── COORDINATOR: Done ─────────────────────────────────────────────
            coordinator_status.update(
                label="✅ Coordinator Agent — Pipeline Complete! All 4 agents finished!",
                state="complete"
            )

        # ── Final Report Section ──────────────────────────────────────────────
        st.divider()
        st.subheader("📄 Final Report")
        st.success("🎉 All 4 agents completed successfully!")

        st.markdown("""
        **🔄 Agent Communication Flow completed:**
        
        `👤 User` → `📋 Coordinator` → `🔍 Research Agent` → `📋 Coordinator` → `✂️ Summarizer Agent` → `📋 Coordinator` → `✅ Reviewer Agent` → `📋 Coordinator` → `📄 Final Report`
        """)

        st.divider()

        # ── Tabs ──────────────────────────────────────────────────────────────
        tab1, tab2, tab3 = st.tabs([
            "📚 Research",
            "📝 Summary",
            "✅ Reviewed & Improved"
        ])

        with tab1:
            st.markdown(research_output)
        with tab2:
            st.markdown(summary_output)
        with tab3:
            st.markdown(review_output)

        # ── Download button ───────────────────────────────────────────────────
        st.divider()
        st.download_button(
            label="⬇️ Download Full Report",
            data=final_report,
            file_name=filename,
            mime="text/plain",
            use_container_width=True
        )
        st.caption(f"💾 Report also saved to: outputs/{filename}")