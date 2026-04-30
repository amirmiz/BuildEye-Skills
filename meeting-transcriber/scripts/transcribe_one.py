"""
Transcribe a single audio file using faster-whisper large-v3.
Usage: python transcribe_one.py <audio_file>

Outputs <audio_file>.txt and <audio_file>.srt in the same directory.
Prints progress every 30 segments so the caller can monitor.
"""
import sys
import os
from pathlib import Path

# ffmpeg PATH injection — winget installs here but running shells may not see it
FFMPEG_BIN = r"C:\Users\1\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1-full_build\bin"
if Path(FFMPEG_BIN).exists() and FFMPEG_BIN not in os.environ.get("PATH", ""):
    os.environ["PATH"] = FFMPEG_BIN + os.pathsep + os.environ.get("PATH", "")

from faster_whisper import WhisperModel


def ts(x: float) -> str:
    """Format seconds as SRT timestamp HH:MM:SS,mmm"""
    h = int(x // 3600)
    m = int((x % 3600) // 60)
    s = x % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}".replace(".", ",")


def transcribe(audio_path: str) -> None:
    audio = Path(audio_path)
    if not audio.exists():
        print(f"ERROR: File not found: {audio_path}", flush=True)
        sys.exit(1)

    print(f"Loading model (large-v3, CPU int8)...", flush=True)
    model = WhisperModel("large-v3", device="cpu", compute_type="int8")

    print(f"Transcribing {audio.name} ...", flush=True)
    segments, info = model.transcribe(
        str(audio),
        language="he",
        vad_filter=True,
        beam_size=5,
    )
    print(f"  duration: {info.duration:.1f}s  lang_prob: {info.language_probability:.2f}", flush=True)

    out_txt = audio.with_suffix(".txt")
    out_srt = audio.with_suffix(".srt")

    with out_txt.open("w", encoding="utf-8") as t, \
         out_srt.open("w", encoding="utf-8") as s:
        for i, seg in enumerate(segments, 1):
            text = seg.text.strip()
            t.write(text + "\n")
            t.flush()
            s.write(f"{i}\n{ts(seg.start)} --> {ts(seg.end)}\n{text}\n\n")
            s.flush()
            if i % 30 == 0:
                print(f"  ... segment {i}, t={seg.end:.0f}s", flush=True)

    print(f"  -> {out_txt.name}, {out_srt.name}", flush=True)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python transcribe_one.py <audio_file>")
        sys.exit(1)
    transcribe(sys.argv[1])
