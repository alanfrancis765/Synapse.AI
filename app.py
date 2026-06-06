import streamlit as st
from LLM import generate_response

st.set_page_config(page_title="Synapse.AI", page_icon="🤖", layout="wide")

#UI part 
st.markdown("""
    <style>
    /* Styling the main title header with a subtle gradient */
    .main-title {
        font-size: 42px !important;
        font-weight: 800 !important;
        background: linear-gradient(45deg, #FF4B4B, #FF8F8F);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    /* Modernizing the chat input background padding */
    .stChatInputContainer {
        padding-bottom: 20px !important;
    }
    /* Adding visual accent borders to the sidebar chat items */
    div[data-testid="stSidebar"] button {
        border-radius: 8px !important;
        transition: all 0.2s ease-in-out;
    }
    div[data-testid="stSidebar"] button:hover {
        transform: scale(1.02);
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar for session management and memory window
if "all_sessions" not in st.session_state:
    st.session_state.all_sessions = {
        "Default chat": []
    }

if "current_session" not in st.session_state:
    st.session_state.current_session = "Default chat"

# active_history = st.session_state.all_sessions[st.session_state.current_session]

with st.sidebar:
    st.markdown("<h2 style='font-weight:700; color:#FF4B4B;'>💬 Synapse Threads</h2>", unsafe_allow_html=True)

    if st.button("➕New Chat", use_container_width=True):
        new_chat_id = f"Chat {len(st.session_state.all_sessions) + 1}"
        st.session_state.all_sessions[new_chat_id] = []
        st.session_state.current_session = new_chat_id
        st.rerun()

    st.write("**Recent Conversations:**")

    for session_name in list(st.session_state.all_sessions.keys()):

        is_active = (session_name == st.session_state.current_session)

        if st.button(
            label=f"{session_name}",
            key=f"button_{session_name}",
            use_container_width=True,
            type="primary" if is_active else "secondary"
        ):
            st.session_state.current_session = session_name
            st.rerun()
    st.markdown("---")

    with st.expander("⚙️Memory Settings"):
        memory_window = st.slider(
            "Memory Window Size", 
            min_value=2, 
            max_value=40, 
            value=20, 
            step=2,
            help="Control how many recent messages the AI considers for generating responses. Adjust based on your conversation length and context needs."
        )
#Main interface UI/UX

st.markdown("<h1 class='main-title'>Synapse.AI</h1>", unsafe_allow_html=True)

current_history = st.session_state.all_sessions[st.session_state.current_session]

# UI UPGRADE: DYNAMIC EMPTY STATE WELCOME SPLASH
# If the active thread has no messages, display a premium minimalist welcoming layout
if len(current_history) == 0:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.info("**Welcome to your fresh workspace!** Type a question or paste a script snippet below to initiate processing context with Synapse AI.")
    
    # Quick suggestion cards for inspiration
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("> **Analyze Core Logistics**\n\n> *'Explain the difference between K-Means and Agglomerative clustering techniques.'*")
    with col2:
        st.markdown("> **Debug Code Structures**\n\n> *'Look over this python script reference variable mapping loop and optimize it.'*")

# Draw the active session's history to screen on refresh
for message in current_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Live User Interaction Loop
if user_input := st.chat_input("Type your message here..."):

    # Display user query instantly
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.all_sessions[st.session_state.current_session].append({"role": "user", "content": user_input})

    # AUTO-RENAME TRICK: Updates "Default Chat" to match your first sentence
    if len(st.session_state.all_sessions[st.session_state.current_session]) == 1:
        clean_title = user_input[:20] + "..." if len(user_input) > 20 else user_input
        
        if clean_title not in st.session_state.all_sessions:
            st.session_state.all_sessions[clean_title] = st.session_state.all_sessions.pop(st.session_state.current_session)
            st.session_state.current_session = clean_title

    # Generate reply using your context limits
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            history_snapshot = st.session_state.all_sessions[st.session_state.current_session].copy()
            recent_context = history_snapshot[-memory_window:]

            ai_reply = generate_response(recent_context)
            st.markdown(ai_reply)
            
    # Append final answer back to active history
    st.session_state.all_sessions[st.session_state.current_session].append({"role": "assistant", "content": ai_reply})
    st.rerun()

