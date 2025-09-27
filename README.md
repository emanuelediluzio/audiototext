Script Python per convertire un file audio lungo (es. 53 minuti) in testo e sottotitoli SRT, con barra di avanzamento percentuale.
Funziona bene su Mac con chip Apple Silicon (M1/M2/M3) utilizzando faster-whisper (consigliato) oppure openai-whisper.

Caratteristiche

Supporto a formati comuni (.m4a, .mp3, .wav, ecc.)

Chunking automatico (audio diviso in parti per robustezza)

Barra di avanzamento con percentuale (tqdm)

Output:

NOMEFILE.trascrizione.txt

NOMEFILE.trascrizione.srt (sottotitoli con timestamp)

Opzioni per lingua, modello, durata chunk

Requisiti

macOS con chip Apple Silicon

Conda o Miniconda

Homebrew (per installare ffmpeg)

FFmpeg

Python 3.10/3.11

Installazione rapida
# 1) Crea ambiente dedicato
conda create -n audio2txt python=3.11 -y
conda activate audio2txt

# 2) FFmpeg (se non presente)
brew install ffmpeg

# 3) Librerie Python
python -m pip install --upgrade pip
python -m pip install pydub tqdm faster-whisper
# In alternativa a faster-whisper:
# python -m pip install openai-whisper


Perché environment dedicato? Evita conflitti con PyTorch/torch/whisper o librerie di sistema (errore tipo libtorch_cpu.dylib not found).

File di esempio

Audio:
/Users/emanuelediluzio/Desktop/4_5960890835586258972.m4a

Script:
/Users/emanuelediluzio/Desktop/audio_to_txt.py

Esecuzione
conda activate audio2txt
python /Users/emanuelediluzio/Desktop/audio_to_txt.py \
  --audio "/Users/emanuelediluzio/Desktop/4_5960890835586258972.m4a" \
  --lang it \
  --model medium \
  --chunk_sec 150


Parametri principali:

--audio (obbligatorio): percorso del file audio.

--lang (opzionale): lingua forzata (es. it, en).

--model (opzionale): modello Whisper.

faster-whisper: tiny, base, small, medium, large-v3 (più grande = più accurato ma più lento).

openai-whisper: tiny, base, small, medium, large-v3.

--chunk_sec (opzionale): durata chunk in secondi (default 120–180 è un buon compromesso).

Output generati accanto al file audio:

4_5960890835586258972.trascrizione.txt

4_5960890835586258972.trascrizione.srt

Nota sui backend

Per impostazione predefinita lo script usa faster-whisper.
Per passare a openai-whisper:

Apri lo script e imposta:

USE_FASTER_WHISPER = False


Installa:

python -m pip install openai-whisper


Consiglio: su M1, faster-whisper con compute_type="int8" è spesso il miglior rapporto velocità/accuratezza.

Struttura dello script

Carica l’audio con pydub

Spezza in chunk da --chunk_sec secondi

Trascrive ogni chunk

Mostra barra di avanzamento (tqdm) in base alla durata totale

Scrive:

testo completo (.txt)

sottotitoli con timestamp (.srt)

Troubleshooting
ModuleNotFoundError: No module named 'faster_whisper'

Installa nel giusto environment:

conda activate audio2txt
python -m pip install faster-whisper

ffmpeg not found

Installa ffmpeg:

brew install ffmpeg


Se ancora non va, aggiungi il path di ffmpeg al tuo $PATH o riavvia il terminale.

Lento / CPU alta

Usa un modello più piccolo (--model small o base)

Aumenta --chunk_sec (es. 180–240) per meno file temporanei

Chiudi app pesanti in background

Errori di permessi sul file audio

Verifica il path e che il file sia leggibile

Evita caratteri speciali non ASCII nei path (se possibile)

Output con punteggiatura scarsa

Prova --model large-v3 (più accurato)

Assicurati di passare --lang it per l’italiano

Esempi
Trascrizione veloce (italiano, modello medio)
python audio_to_txt.py \
  --audio "/Users/emanuelediluzio/Desktop/4_5960890835586258972.m4a" \
  --lang it --model medium --chunk_sec 150

Massima qualità (lento)
python audio_to_txt.py \
  --audio "/Users/emanuelediluzio/Desktop/4_5960890835586258972.m4a" \
  --lang it --model large-v3 --chunk_sec 180

Inglese, chunk più corti
python audio_to_txt.py \
  --audio "/path/to/file.mp3" \
  --lang en --model small --chunk_sec 90

FAQ

Posso usare Qwen3-Omni-30B-A3B-Captioner?
Non in locale su M1 in modo pratico: è un 30B pensato per GPU grandi e accetta solo ~30s per inferenza. Per trascrizione ASR la scelta più semplice/robusta è Whisper.

Dove trovo i file di output?
Nella stessa cartella del file audio, con suffissi .trascrizione.txt e .trascrizione.srt.

Supporta file lunghi (>1h)?
Sì, il chunking li gestisce senza problemi (dipende da spazio e tempo di calcolo).

Licenza

Questo repository è distribuito con licenza MIT
