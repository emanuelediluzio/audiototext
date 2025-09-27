import os
import math
import argparse
from datetime import timedelta

from pydub import AudioSegment
from tqdm import tqdm

# ====== Scegli il backend di trascrizione ======
USE_FASTER_WHISPER = True  # True: faster-whisper, False: openai-whisper

if USE_FASTER_WHISPER:
    from faster_whisper import WhisperModel
else:
    import whisper


def format_timestamp(seconds: float) -> str:
    """SRT timestamp (HH:MM:SS,mmm)"""
    td = timedelta(seconds=seconds)
    total_ms = int(td.total_seconds() * 1000)
    hrs = total_ms // 3600000
    mins = (total_ms % 3600000) // 60000
    secs = (total_ms % 60000) // 1000
    ms = total_ms % 1000
    return f"{hrs:02}:{mins:02}:{secs:02},{ms:03}"


def write_srt(segments, srt_path):
    with open(srt_path, "w", encoding="utf-8") as f:
        for i, seg in enumerate(segments, start=1):
            start, end, text = seg
            f.write(f"{i}\n")
            f.write(f"{format_timestamp(start)} --> {format_timestamp(end)}\n")
            f.write(text.strip() + "\n\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--audio", required=True, help="Percorso del file audio (es. .mp3, .wav)")
    parser.add_argument("--lang", default=None, help="Lingua forzata (es. it, en). Opzionale.")
    parser.add_argument("--model", default="medium", help="Modello whisper (tiny/base/small/medium/large-v3).")
    parser.add_argument("--chunk_sec", type=int, default=120, help="Lunghezza chunk in secondi (default: 120).")
    args = parser.parse_args()

    audio_path = args.audio
    if not os.path.isfile(audio_path):
        raise FileNotFoundError(f"Audio non trovato: {audio_path}")

    # Carica audio intero
    audio = AudioSegment.from_file(audio_path)
    total_ms = len(audio)
    chunk_ms = args.chunk_sec * 1000
    num_chunks = math.ceil(total_ms / chunk_ms)

    # Prepara modelli
    if USE_FASTER_WHISPER:
        # device="auto" sceglie MPS se disponibile su Mac
        model = WhisperModel(args.model, device="auto", compute_type="int8")  # int8 = veloce e leggero
        transcribe_fn = lambda wav_path: list(
            model.transcribe(
                wav_path,
                language=args.lang,
                beam_size=5,
                vad_filter=True,
                vad_parameters=dict(min_silence_duration_ms=500),
            )[0]
        )
    else:
        model = whisper.load_model(args.model)  # es. "medium"
        def transcribe_fn(wav_path):
            result = model.transcribe(wav_path, language=args.lang)
            # Adattiamo al formato (start, end, text)
            return [
                type("Seg", (), {"start": s["start"], "end": s["end"], "text": s["text"]})
                for s in result["segments"]
            ]

    # Trascrizione per chunk con barra percentuale
    all_text = []
    srt_segments = []
    print(f"Trascrizione in corso... ({num_chunks} chunk da ~{args.chunk_sec}s)")

    # Base filename per output
    base_out = os.path.splitext(os.path.basename(audio_path))[0]
    txt_out = f"{base_out}.trascrizione.txt"
    srt_out = f"{base_out}.trascrizione.srt"

    with tqdm(total=total_ms, unit="ms") as pbar:
        processed_ms = 0
        for i in range(num_chunks):
            start_ms = i * chunk_ms
            end_ms = min((i + 1) * chunk_ms, total_ms)
            chunk = audio[start_ms:end_ms]

            tmp_wav = f"_chunk_{i}.wav"
            chunk.export(tmp_wav, format="wav")

            # Trascrivi il chunk
            segments = transcribe_fn(tmp_wav)

            # Accumula testo e segmenti SRT (shiftando di start_ms)
            for seg in segments:
                seg_start = (seg.start or 0.0) + (start_ms / 1000.0)
                seg_end = (seg.end or seg_start) + (start_ms / 1000.0)
                seg_text = seg.text if hasattr(seg, "text") else getattr(seg, "text", "")
                all_text.append(seg_text)
                srt_segments.append((seg_start, seg_end, seg_text))

            os.remove(tmp_wav)

            # Aggiorna barra (percentuale basata sul tempo totale)
            pbar.update(end_ms - processed_ms)
            processed_ms = end_ms

    # Salva output
    with open(txt_out, "w", encoding="utf-8") as f:
        f.write("\n".join(t.strip() for t in all_text if t and t.strip()))

    write_srt(srt_segments, srt_out)

    print(f"✅ Fatto!\n- Testo: {os.path.abspath(txt_out)}\n- Sottotitoli SRT: {os.path.abspath(srt_out)}")


if __name__ == "__main__":
    main()
