import streamlit as st
import backend.auth_backend as bot_auth
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
    /* Custom container style for premium login cards */
    .auth-box {
        background-color: #1E1E1E;
        padding: 30px;
        border-radius: 12px;
        border: 1px solid #333333;
    }
    </style>
""", unsafe_allow_html=True)

# Authentication and session management
if "auth_status" not in st.session_state:
    st.session_state.auth_status = None
    
if "auth_method" not in st.session_state:
    st.session_state.auth_method = None 

if "all_sessions" not in st.session_state:
    st.session_state.all_sessions = {
        "Default Chat": []
    }
if "current_session" not in st.session_state:
    st.session_state.current_session = "Default Chat"

#Intercept traffic with the authentication gateway
if st.session_state.auth_status is None:
    _, col, _ = st.columns([1, 1.3, 1])

    with col:
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Start a clean styling block matching your image layout
        with st.container(border=True):
            st.markdown("<h3 style='margin-bottom:15px; font-weight:700;'>Login / Signup</h3>", unsafe_allow_html=True)
            
            # Simple Mode Selection dropdown
            auth_mode = st.selectbox("Action", ["Login", "Sign Up"], label_visibility="collapsed")
            
            # Form fields
            email_input = st.text_input("Email Address", placeholder="Enter your email")
            password_input = st.text_input("Password", type="password", placeholder="Enter your password")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Action button
            button_label = "Login" if auth_mode == "Login" else "Register"
            if st.button(button_label, type="primary", use_container_width=True):
                if email_input.strip() and password_input.strip():
                    
                    # Call your backend handshake
                    uid = bot_auth.sign_in_or_register_email(
                        email=email_input.strip(),
                        password=password_input.strip(),
                        mode=auth_mode
                    )
                    
                    if uid:
                        st.session_state.auth_status = "verified"
                        st.session_state.user_profile = {"display_name": email_input.strip(), "uid": uid}

                        # Hydrate database data directly out of your custom named database
                        st.session_state.all_sessions = bot_auth.load_user_sessions(uid)
                        st.session_state.current_session = list(st.session_state.all_sessions.keys())[0]
                        st.rerun()
                else:
                    st.error("Please fill out both email and password fields.")
                    
    st.stop()



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
        display_name = session_name if len(session_name) < 22 else session_name[:20] + "..."

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
            help="Control how many recent messages the AI considers for generating responses."
        )

    st.markdown("---")

    if st.button("🚪 Logout", use_container_width=True):
        bot_auth.process_clear_logout()
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

    if st.session_state.current_session == "Default Chat" and len(st.session_state.all_sessions["Default Chat"]) == 1:
        clean_title = user_input[:20] + "..." if len(user_input) > 20 else user_input
        if clean_title not in st.session_state.all_sessions:
            st.session_state.all_sessions[clean_title] = st.session_state.all_sessions.pop("Default Chat")
            st.session_state.current_session = clean_title

    # Save the user message to Firebase under the finalized session key
    bot_auth.save_chat_message(
        st.session_state.user_profile["uid"],
        st.session_state.current_session,
        "user",
        user_input
    )

    # Generate reply using context limits
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Thinking..."):
            history_snapshot = st.session_state.all_sessions[st.session_state.current_session].copy()
            recent_context = history_snapshot[-memory_window:]

            ai_reply = generate_response(recent_context)
            st.markdown(ai_reply)
            
    # Append final answer back to active history
    st.session_state.all_sessions[st.session_state.current_session].append({"role": "assistant", "content": ai_reply})

    # Save assistant response to Firebase
    bot_auth.save_chat_message(
        st.session_state.user_profile["uid"],
        st.session_state.current_session,
        "assistant",
        ai_reply
    )
    st.rerun()