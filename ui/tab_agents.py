import json
import streamlit as st
from core.agents import (
    get_agent_tools, 
    get_react_prompt, 
    StreamlitTraceCallback, 
    AgentExecutor, 
    create_react_agent,
    run_agent_execution
)
from core.workflows import build_support_router_graph

def render_tab_agents(get_llm_fn):
    st.markdown('<div class="tab-header">Agentic Orchestration (LangChain & LangGraph)</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([6, 6])
    
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("LangChain ReAct Agent Executor")
        st.caption("Demonstrate how LLMs choose tools using the Thought-Action-Observation loop.")
        
        agent_input = st.text_input("Ask Agent (Tool usage query)", "What is the time right now, and what is 123 * 45?")
        
        if st.button("Run ReAct Agent"):
            tools_list = get_agent_tools()
            prompt_tpl = get_react_prompt()
            
            log_container = st.empty()
            logs = []
            
            llm = get_llm_fn()
            st.write("#### Execution Trace Logs")
            try:
                cb = StreamlitTraceCallback(log_container, logs)
                answer = run_agent_execution(llm, tools_list, prompt_tpl, agent_input, cb)
                st.success(f"**Final Answer**: {answer}")
            except Exception as e:
                st.error(f"Agent execution error: {str(e)}")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("LangGraph Support Ticket Router")
        st.caption("Observe structured routing workflows. Enter a support request to simulate graph nodes.")
        
        ticket_query = st.text_input("Customer Support Ticket Description", "I need to get a refund for my billing plan from last month.")
        
        if st.button("Process in LangGraph StateGraph"):
            st.write("#### Flow Sequence State Updates")
            
            graph = build_support_router_graph()
            initial_state = {
                "ticket": ticket_query, 
                "category": "", 
                "assigned": "", 
                "messages": ["State initialized."]
            }
            
            for event in graph.stream(initial_state):
                for node_name, state_update in event.items():
                    st.markdown(f"""
                    <div style="background: rgba(139, 92, 246, 0.1); border: 1px solid rgba(139, 92, 246, 0.25); border-radius: 8px; padding: 12px; margin-bottom: 10px;">
                        <div style="font-weight: bold; color: #a78bfa; margin-bottom: 3px;">[Active Node: {node_name.upper()}]</div>
                        <div style="font-size: 11px; color: #9ca3af; font-family: monospace;">State parameters updated: {json.dumps(state_update)}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
            final_res = graph.invoke(initial_state)
            st.success(f"**Ticket Routing Completed**! Assigned to: `{final_res['assigned']}`")
        st.markdown('</div>', unsafe_allow_html=True)
