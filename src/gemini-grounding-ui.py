import json
import os
import streamlit as st
from google import genai
from google.genai.types import Content, GenerateContentConfig, GoogleSearch, Part, Tool


def main():
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", ""))

    st.title("Gemini Grounding UI")
    clear = st.button("Clear Chat History")
    use_config = st.checkbox("Use Grounding", value=True)

    if clear or "messages" not in st.session_state:
        st.session_state.messages = []

    # Extract and display content from messages
    for message in st.session_state.messages:
        role = "assistant" if message["content"].role == "model" else message["content"].role

        with st.chat_message(role):
            st.markdown(message["content"].parts[0].text)

        if message["grounding_links"]:
            st.markdown(message["grounding_links"])

        if message["grounding_queries"]:
            st.text("Query: " + message["grounding_queries"])

    # Chat input
    if message_user := st.chat_input("Ask a question"):
        st.session_state.messages.append({
            "content": Content(role="user", parts=[Part.from_text(message_user)]),
            "grounding_links": "",
            "grounding_queries": ""
        })

        with st.chat_message("user"):
            st.markdown(message_user)

        with st.chat_message("assistant"):
            message_assistant = st.empty()

        contents = [message["content"]
                    for message in st.session_state.messages]

        # Generate content
        response_stream = client.models.generate_content_stream(
            model="gemini-2.0-flash",
            contents=contents,
            config=GenerateContentConfig(
                tools=[Tool(google_search=GoogleSearch())]) if use_config else None
        )

        response_text = ""
        grounding_links = ""
        grounding_queries = ""

        # Display response
        for response_chunk in response_stream:
            response = response_chunk

            if response_chunk.text:
                response_text += response_chunk.text
                message_assistant.markdown(response_text)

        # Display grounding metadata
        if response and response.candidates and response.candidates[0].grounding_metadata:
            if response.candidates[0].grounding_metadata.grounding_chunks:
                for i, grounding_chunk in enumerate(response.candidates[0].grounding_metadata.grounding_chunks):
                    if grounding_chunk.web:
                        grounding_links += f"[{i + 1}][{grounding_chunk.web.title}]({
                            grounding_chunk.web.uri}) "

                st.markdown(grounding_links)

            if response.candidates[0].grounding_metadata.web_search_queries:
                for web_search_query in response.candidates[0].grounding_metadata.web_search_queries:
                    grounding_queries += f"{web_search_query} / "

                st.text("Query: " + grounding_queries.rstrip(" /"))

        # Append response to chat history
        st.session_state.messages.append({
            "content": Content(role="model", parts=[Part.from_text(response_text)]),
            "grounding_links": grounding_links,
            "grounding_queries": grounding_queries
        })

        print(json.dumps(response.model_dump(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
