# Trascrizione Audio con Whisper

Questo progetto utilizza il modello Whisper di OpenAI per trascrivere file audio. Whisper è un modello di intelligenza artificiale potente e versatile addestrato per convertire l'audio in testo. Questa implementazione specifica permette di convertire file audio di vari formati in testo, assicurando che il file audio sia nel formato e nel tasso di campionamento corretti prima della trascrizione.

## Requisiti

Per utilizzare questo progetto, è necessario installare alcune dipendenze. Assicurati di avere Python installato sul tuo sistema e poi installa i seguenti pacchetti utilizzando `pip`:

- `transformers`
- `librosa`
- `pydub`
- `ffmpeg`

Puoi installare le dipendenze necessarie con il seguente comando:

pip install transformers librosa pydub
Nota: ffmpeg deve essere installato separatamente. Puoi trovare le istruzioni per l'installazione su FFmpeg.org.(per Mac basato su ARM: https://github.com/ssut/ffmpeg-on-apple-silicon)

Utilizzo

Il codice principale esegue le seguenti operazioni:

Conversione del File Audio: Converti il file audio dal formato originale (ad es., .m4a) in .wav utilizzando pydub. Questo passaggio è necessario perché la libreria soundfile (usata internamente da librosa) non supporta il formato .m4a.
Caricamento e Pre-elaborazione dell'Audio: Carica il file audio convertito utilizzando librosa, impostando il tasso di campionamento a 16.000 Hz, che è il tasso richiesto dal modello Whisper.
Trascrizione: Utilizza il modello Whisper per generare la trascrizione del file audio.
Pulizia: Elimina il file .wav temporaneo per mantenere pulito il filesystem.
