import streamlit as st
from nltk.chat.util import Chat, reflections

# Pairs (copied from your file)
pairs = [
    [
        r"(.*)my name is (.*)",
        ["Hello %2, How are you today ?"]
    ],
    [
        r"(.*)help(.*)",
        ["I can help you "]
    ],
    [
        r"(.*) your name ?",
        ["My name is thecleverprogrammer, but you can just call me robot and I'm a chatbot."]
    ],
    [
        r"how are you (.*) ?",
        ["I'm doing very well", "I am great !"]
    ],
    [
        r"sorry (.*)",
        ["Its alright","Its OK, never mind that"]
    ],
    [
        r"i'm (.*) (good|well|okay|ok)",
        ["Nice to hear that","Alright, great !"]
    ],
    [
        r"(hi|hey|hello|hola|holla)(.*)",
        ["Hello", "Hey there"]
    ],
    [
        r"what (.*) want ?",
        ["Make me an offer I can't refuse"]
    ],
    [
        r"(.*)created(.*)",
        ["Ronita created me using Python's NLTK library","Top secret ;)"]
    ],
    [
        r"(.*) (location|city) ?",
        ['Kolkata, India']
    ],
    [
        r"(.*)raining in (.*)",
        ["No rain in the past 4 days here in %2","In %2 there is a 50% chance of rain"]
    ],
    [
        r"how (.*) health (.*)",
        ["Health is very important, but I am a computer, so I don't need to worry about my health "]
    ],
    [
        r"(.*)(sports|game|sport)(.*)",
        ["I'm a very big fan of Cricket"]
    ],
    [
        r"who (.*) (Cricketer|Batsman)?",
        ["Virat Kohli"]
    ],
    [
        r"quit",
        ["Bye for now. See you soon :)","It was nice talking to you. See you soon :)"]
    ],
    [
        r"(.*)",
        ['Our customer service will reach you']
    ]
]

# Create chatbot
chatbot = Chat(pairs, reflections)

# ---------------- Streamlit UI ----------------
st.set_page_config(page_title="Chatbot", page_icon="🤖")
st.title("🤖 Chatbot App")
st.write("Type your message and chat with the bot!")

# Chat history
if "history" not in st.session_state:
    st.session_state.history = []

# User input
user_input = st.text_input("You:", "")

if user_input:
    response = chatbot.respond(user_input)
    st.session_state.history.append(("You", user_input))
    st.session_state.history.append(("Bot", response))

# Display chat history
for speaker, message in st.session_state.history:
    if speaker == "You":
        st.markdown(f"**👤 You:** {message}")
    else:
        st.markdown(f"**🤖 Bot:** {message}")