"""
Blog to Voiceover — free, unlimited alternative to sites like aiktp.com.

Paste blog text, pick a natural-sounding voice (including Australian English),
generate a ready-to-download MP3. Runs on Hugging Face Spaces' free tier —
one shared link, no installs, nothing for teammates to set up.

Powered by edge-tts, an open-source library built on the same free neural
voices behind Microsoft Edge's "Read Aloud" feature. No API key, no account,
no per-use cost.
"""

import asyncio
import re
import tempfile

import edge_tts
import gradio as gr

VOICES = {
    "Natasha — Australian English (Female)": "en-AU-NatashaNeural",
    "William — Australian English (Male)": "en-AU-WilliamMultilingualNeural",
    "Sonia — British English (Female)": "en-GB-SoniaNeural",
    "Ryan — British English (Male)": "en-GB-RyanNeural",
    "Aria — American English (Female)": "en-US-AriaNeural",
    "Guy — American English (Male)": "en-US-GuyNeural",
    "Jenny — American English (Female, conversational)": "en-US-JennyNeural",
    "Neerja — Indian English (Female)": "en-IN-NeerjaNeural",
    "Prabhat — Indian English (Male)": "en-IN-PrabhatNeural",
}


def clean_text(raw: str) -> str:
    """Strip HTML tags/entities in case rich blog HTML gets pasted in,
    and collapse whitespace so pauses land naturally between paragraphs."""
    text = re.sub(r"<[^>]+>", " ", raw)
    text = re.sub(r"&nbsp;|&amp;|&quot;|&#39;", " ", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    return text.strip()


def generate_voiceover(text, voice_label, speed):
    if not text or not text.strip():
        raise gr.Error("Paste some blog text first.")
    if len(text) > 50000:
        raise gr.Error("That's a lot of text — please keep it under 50,000 characters per run.")

    voice = VOICES.get(voice_label, "en-AU-NatashaNeural")
    rate = f"{'+' if speed >= 0 else ''}{speed}%"
    cleaned = clean_text(text)

    out_path = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False).name

    async def synthesize():
        communicate = edge_tts.Communicate(cleaned, voice=voice, rate=rate)
        await communicate.save(out_path)

    try:
        asyncio.run(synthesize())
    except Exception as e:
        raise gr.Error(f"Couldn't generate audio: {e}")

    return out_path


with gr.Blocks(title="Blog to Voiceover") as demo:
    gr.Markdown(
        "# Blog to Voiceover\n"
        "Paste your blog text, pick a voice, generate a natural-sounding MP3. "
        "Free, unlimited, no login needed."
    )
    with gr.Row():
        with gr.Column(scale=2):
            text_in = gr.Textbox(
                label="Blog text",
                placeholder="Paste your blog post here...",
                lines=14,
            )
        with gr.Column(scale=1):
            voice_in = gr.Dropdown(
                label="Voice",
                choices=list(VOICES.keys()),
                value="Natasha — Australian English (Female)",
            )
            speed_in = gr.Slider(
                label="Speed adjustment (%)",
                minimum=-30,
                maximum=30,
                value=0,
                step=5,
            )
            generate_btn = gr.Button("Generate voiceover", variant="primary")

    audio_out = gr.Audio(label="Voiceover", type="filepath")

    generate_btn.click(
        fn=generate_voiceover,
        inputs=[text_in, voice_in, speed_in],
        outputs=audio_out,
    )

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 7860))
    demo.launch(server_name="0.0.0.0", server_port=port)
