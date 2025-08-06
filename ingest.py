import yt_dlp
import whisper
from pathlib import Path

def download_and_transcribe(url, output_dir="memory"):
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_dir}/%(id)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        video_id = info["id"]
        mp3_path = output_dir / f"{video_id}.mp3"
    
    if not mp3_path.exists():
        raise FileNotFoundError(f"Expected audio file not found: {mp3_path}")

    model = whisper.load_model("small")
    result = model.transcribe(str(mp3_path))

    # Save transcript
    transcript_path = output_dir / f"{video_id}.txt"
    transcript_path.write_text(result["text"])

    # Save video index for sidebar
    index_path = output_dir / "video_index.txt"
    with index_path.open("a") as f:
        f.write(f"{video_id}|{info['title']}|{info['webpage_url']}\n")

    return video_id, result["text"]
