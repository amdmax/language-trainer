#!/usr/bin/env python3
"""
Usage: printf '%s' "text" | .venv/bin/python3 tts.py --lang <es|ro>
Text is read from stdin to safely handle quotes and diacritics.
"""
import sys, os, argparse, tempfile, subprocess, asyncio

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--lang", required=True, choices=["es", "ro"])
    p.add_argument("--voice", default=None)
    return p.parse_args()

def read_stdin():
    text = sys.stdin.read().strip()
    if not text:
        sys.exit(0)
    return text

def synthesize_spanish(text, voice="ef_dora"):
    from kokoro import KPipeline
    import soundfile as sf
    import numpy as np
    pipeline = KPipeline(lang_code="e")
    chunks = [audio for _, _, audio in pipeline(text, voice=voice) if audio is not None and len(audio) > 0]
    if not chunks:
        sys.exit(1)
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False, prefix="tts_es_")
    sf.write(tmp.name, np.concatenate(chunks), samplerate=24000)
    return tmp.name

async def _ro_async(text, voice, path):
    import edge_tts
    await edge_tts.Communicate(text, voice).save(path)

def synthesize_romanian(text, voice="ro-RO-EmilNeural"):
    tmp = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False, prefix="tts_ro_")
    path = tmp.name
    tmp.close()
    asyncio.run(_ro_async(text, voice, path))
    return path

def play_and_cleanup(path):
    import shlex
    subprocess.Popen(
        f"afplay {shlex.quote(path)} && rm -f {shlex.quote(path)}",
        shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        start_new_session=True,
    )

def main():
    args = parse_args()
    text = read_stdin()
    if args.lang == "es":
        audio = synthesize_spanish(text, voice=args.voice or "ef_dora")
    else:
        audio = synthesize_romanian(text, voice=args.voice or "ro-RO-EmilNeural")
    play_and_cleanup(audio)

if __name__ == "__main__":
    main()
