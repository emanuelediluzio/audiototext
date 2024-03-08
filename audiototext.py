from transformers import WhisperProcessor, WhisperForConditionalGeneration
from pydub import AudioSegment
import librosa
import os  # Modulo per interagire con il sistema operativo

# Converti il file .m4a in .wav utilizzando pydub
file_audio_path = "nomefileaudio"
audio_segment = AudioSegment.from_file(file_audio_path)
file_audio_path_wav = "audio.wav"
audio_segment.export(file_audio_path_wav, format="wav")

# Carica l'audio convertito utilizzando librosa
audio, sampling_rate = librosa.load(file_audio_path_wav, sr=16000)  # Già impostato su 16000 Hz

# load model and processor
processor = WhisperProcessor.from_pretrained("openai/whisper-large-v2")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-large-v2")

# Prepara i dati audio per il modello
input_features = processor(audio, sampling_rate=sampling_rate, return_tensors="pt").input_features

# Genera gli ID dei token
predicted_ids = model.generate(input_features)

# Decodifica gli ID dei token in testo
transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)

print(transcription)

# Elimina il file .wav temporaneo
os.remove(file_audio_path_wav)
