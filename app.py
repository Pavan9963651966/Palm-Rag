import streamlit as st
from src.helper import get_pdf_text, get_text_chunks, get_vector_store, get_conversational_chain

# Add custom CSS to enhance the UI
def add_custom_css():
    st.markdown(
        """
        <style>
        body {
            background-color: #e0f7fa;
        }
        .main-content {
            background: linear-gradient(135deg, #ffffff, #e0f7fa);
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.1);
        }
        .sidebar-content {
            background: linear-gradient(135deg, #f3e5f5, #d1c4e9);
            padding: 20px;
            border-radius: 15px;
        }
        .header {
            font-size: 40px;
            color: #00796b;
            font-weight: bold;
            text-align: center;
            margin-bottom: 20px;
            text-shadow: 2px 2px #81d4fa;
        }
        .sub-header {
            color: #004d40;
            text-align: center;
            margin-bottom: 30px;
            font-style: italic;
        }
        .custom-button {
            background-color: #0288d1;
            color: white;
            padding: 12px 25px;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
            margin-top: 15px;
        }
        .custom-button:hover {
            background-color: #0277bd;
        }
        .chat-bubble {
            background-color: #ffecb3;
            padding: 15px;
            border-radius: 15px;
            margin-bottom: 10px;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
        }
        .chat-bubble.user {
            background-color: #dcedc8;
        }
        .chat-bubble.reply {
            background-color: #b2ebf2;
        }
        </style>
        """, unsafe_allow_html=True
    )

def user_input(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chatHistory = response['chat_history']
    for i, message in enumerate(st.session_state.chatHistory):
        if i % 2 == 0:
            st.markdown(f"<div class='chat-bubble user'>🧑 **User**: {message.content}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-bubble reply'>🤖 **Reply**: {message.content}</div>", unsafe_allow_html=True)

def main():
    st.set_page_config("Information Retrieval System", page_icon="✨", layout="wide")
    add_custom_css()

    # Colorful header and sub-header
    st.markdown('<div class="header">✨ Information Retrieval System 💡</div>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Your go-to tool for interactive question-answering from PDFs.</p>', unsafe_allow_html=True)

    # User input section with placeholder
    user_question = st.text_input("❓ Ask a Question from the PDF Files", placeholder="e.g., What are the main points of the document?")

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chatHistory" not in st.session_state:
        st.session_state.chatHistory = None
    if user_question:
        user_input(user_question)

    with st.sidebar:
        st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
        st.title("📁 Upload & Process")
        pdf_docs = st.file_uploader("Upload your PDF Files", accept_multiple_files=True)
        if st.button("Submit & Process", key="process"):
            with st.spinner("Processing your PDFs..."):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                vector_store = get_vector_store(text_chunks)
                st.session_state.conversation = get_conversational_chain(vector_store)
                st.success("Processing complete! 🎉")
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()



