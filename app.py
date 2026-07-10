"""Streamlit UI for the Multimodal Visual Analyst.

Upload an image, then either ask free-form questions about it or run a one-click
structured analysis. Run:  streamlit run app.py
"""
from __future__ import annotations

import streamlit as st

import config
from vision import client
from vision.analyze import analyze
from vision.qa import answer

st.set_page_config(
    page_title="Multimodal Visual Analyst",
    page_icon=":material/visibility:",
    layout="wide",
)

# ---- session state ----
if "chat" not in st.session_state:
    st.session_state.chat = []  # list of {role, text}
if "image_key" not in st.session_state:
    st.session_state.image_key = None


def _load_image() -> tuple[bytes, str, str] | None:
    """Sidebar uploader. Returns (bytes, data_url, name) or None."""
    with st.sidebar:
        st.subheader(":material/image: Your image")
        uploaded = st.file_uploader("Upload an image", type=list(config.ALLOWED_TYPES))
        if not uploaded:
            st.caption("PNG, JPG, or WebP · up to 4 MB")
            return None

        data = uploaded.getvalue()
        size_mb = len(data) / (1024 * 1024)
        if size_mb > config.MAX_IMAGE_MB:
            st.error(f"Image is {size_mb:.1f} MB — please use one under {config.MAX_IMAGE_MB} MB.")
            return None

        # Reset the conversation when a new image is loaded.
        if uploaded.name != st.session_state.image_key:
            st.session_state.chat = []
            st.session_state.image_key = uploaded.name

        st.image(data, caption=uploaded.name, use_container_width=True)
        st.divider()
        if not config.GROQ_API_KEY:
            st.error("GROQ_API_KEY missing — set it in your .env file.")
        else:
            st.caption(f"Model: `{config.VISION_MODEL}`")

        data_url = client.encode_image(data, client.mime_for(uploaded.name))
        return data, data_url, uploaded.name


def _render_analysis(a) -> None:
    st.markdown(f"**Description** — {a.description}")
    cols = st.columns(2)
    with cols[0]:
        if a.objects:
            st.markdown("**Objects / elements**")
            st.write(", ".join(a.objects))
        if a.colors:
            st.markdown("**Dominant colors**")
            st.write(", ".join(a.colors))
    with cols[1]:
        if a.text_in_image:
            st.markdown("**Text found in image**")
            for t in a.text_in_image:
                st.write(f"- {t}")
    if a.key_insights:
        st.markdown("**Key insights**")
        for k in a.key_insights:
            st.write(f"- {k}")
    with st.expander("Raw JSON"):
        st.json(
            {
                "description": a.description,
                "objects": a.objects,
                "text_in_image": a.text_in_image,
                "colors": a.colors,
                "key_insights": a.key_insights,
            }
        )


def main() -> None:
    st.title("Multimodal Visual Analyst")
    st.caption(
        "Upload an image, then **ask questions** about it or run a one-click "
        "**structured analysis** that turns the picture into clean JSON."
    )

    loaded = _load_image()

    if loaded is None:
        st.info("Upload an image from the sidebar to begin.")
        return
    if not config.GROQ_API_KEY:
        st.error("Set GROQ_API_KEY in .env to run the analyst.")
        return

    _data, data_url, _name = loaded

    # --- Structured analysis ---
    if st.button("Run structured analysis", type="primary"):
        with st.spinner("Analyzing image…"):
            result = analyze(data_url)
        _render_analysis(result)
        st.divider()

    # --- Chat history ---
    for turn in st.session_state.chat:
        with st.chat_message(turn["role"]):
            st.markdown(turn["text"])

    # --- New question ---
    question = st.chat_input("Ask about the image…")
    if not question:
        return

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Looking…"):
            reply = answer(data_url, question, st.session_state.chat)
        st.markdown(reply)

    st.session_state.chat.append({"role": "user", "text": question})
    st.session_state.chat.append({"role": "assistant", "text": reply})


if __name__ == "__main__":
    main()
