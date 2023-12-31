import google.generativeai as genai
import streamlit as st

from PIL import Image
from streamlit_tags import st_tags

st.title("Takon")

# Initialize Google API
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)

col1, col2 = st.columns(2)

with col1:
    with st.expander("Model settings"):
        model_selected = st.selectbox(
            label="Model",
            options=("gemini-pro", "gemini-pro-vision"),
            placeholder="Select a model",
            label_visibility="collapsed",
        )

        # Define state session of the model
        st.session_state["model"] = model_selected

        if st.session_state["model"] == "gemini-pro" or st.session_state["model"] == "gemini-pro-vision":
            model = genai.GenerativeModel(st.session_state["model"])

            if st.session_state["model"] == "gemini-pro":
                max_output_tokens_value = 2048
                top_k_value = 1
            else:
                max_output_tokens_value = 4096
                top_k_value = 32

            # The help section for each component is taken from https://ai.google.dev/docs/concepts#model_parameters
            temperature = st.slider(
                label="Temperature",
                min_value=0.0,
                max_value=1.0,
                value=0.9,
                step=0.1,
                help="The temperature controls the degree of randomness in token selection. The temperature "
                     "is used for sampling during response generation, which occurs when topP and topK are "
                     "applied. Lower temperatures are good for prompts that require a more deterministic or "
                     "less open-ended response, while higher temperatures can lead to more diverse or creative "
                     "results. A temperature of 0 is deterministic, meaning that the highest probability "
                     "response is always selected."
            )
            max_output_tokens = st.number_input(
                label="Max output token",
                min_value=1,
                max_value=max_output_tokens_value,
                value=max_output_tokens_value,
                step=1,
                help="Specifies the maximum number of tokens that can be generated in the response. A token "
                     "is approximately four characters. 100 tokens correspond to roughly 60-80 words."
            )
            top_k = st.number_input(
                label="Top K",
                min_value=1,
                value=top_k_value,
                step=1,
                help="The topK parameter changes how the model selects tokens for output. A topK of 1 means "
                     "the selected token is the most probable among all the tokens in the model's vocabulary "
                     "(also called greedy decoding), while a topK of 3 means that the next token is selected "
                     "from among the 3 most probable using the temperature. For each token selection step, "
                     "the topK tokens with the highest probabilities are sampled. Tokens are then further "
                     "filtered based on topP with the final token selected using temperature sampling."
            )
            top_p = st.slider(
                label="Top P",
                min_value=0.1,
                max_value=1.0,
                value=1.0,
                step=0.1,
                help="The topP parameter changes how the model selects tokens for output. Tokens are "
                     "selected from the most to least probable until the sum of their probabilities equals "
                     "the topP value. For example, if tokens A, B, and C have a probability of 0.3, 0.2, "
                     "and 0.1 and the topP value is 0.5, then the model will select either A or B as the "
                     "next token by using the temperature and exclude C as a candidate. The default topP "
                     "value is 0.95."

            )
            stop_sequences = st_tags(
                label="Stop sequence",
                text="Press enter to add",
                value=None,
                maxtags=5,
            )

            # Configuration for model settings and outputs
            generation_config = genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_output_tokens,
                top_k=top_k,
                top_p=top_p,
                stop_sequences=stop_sequences,
            )

# Image input form
if st.session_state["model"] == "gemini-pro-vision":
    if file := st.file_uploader(label="Upload an image"):
        image_file = Image.open(file)
        st.image(image_file)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
    })

    # Display use message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        messages = [
            {
                "role": message["role"],
                "parts": message["content"]
            }
            for message in st.session_state.messages
        ]

        with st.spinner("Wait for it..."):
            if st.session_state["model"] == "gemini-pro":
                # The gemini-pro model can handle a multi-turn conversational format. This
                # model only accepts text as input.
                response = model.generate_content(
                    contents=messages,
                    generation_config=generation_config,
                )

            elif st.session_state["model"] == "gemini-pro-vision":
                # The gemini-pro-vision model does not handle multi-turn conversational formats.
                # But, it accepts multimodal input in the form of images and text. Therefore,
                # for this model, only single-turn chats can be conducted.
                #
                # However, the application can still receive input in the form of the next chat, but
                # the text input value used is only the last chat.
                response = model.generate_content(
                    contents=[st.session_state.messages[-1]["content"], image_file],
                    generation_config=generation_config,
                )
            message_placeholder.markdown(response.text)

    # Add assistant response to chat history
    st.session_state.messages.append({
        "role": "model",
        "content": response.text,
    })
