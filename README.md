# 🎬 Video2Faces

**Estrazione automatica di volti da file video con generazione di report HTML**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Linux%20|%20Windows%20WSL%20|%20macOS-lightgrey.svg)]()

Video2Faces è uno strumento per l'analisi forense e la computer vision che estrae automaticamente i volti da file video, salvando sia i frame completi che i ritagli dei singoli volti, generando un report HTML interattivo.

![Demo](https://img.shields.io/badge/Demo-Screenshot-green)

## ✨ Caratteristiche

- 🔍 **Rilevamento volti** con modelli CNN (accurato) o HOG (veloce)
- 🖼️ **Salvataggio frame** completi e ritagli dei volti
- 📊 **Report HTML** interattivo con anteprime e statistiche
- ⏱️ **Naming convention** basata su timestamp video (hh_mm_ss_frame.png)
- 📁 **Organizzazione automatica** in directory separate
- 🎛️ **Opzioni flessibili** per ottimizzare velocità/accuratezza
- 🖥️ **Visualizzazione live** durante l'elaborazione

## 📋 Requisiti

- Python 3.8 o superiore
- CMake
- Compilatore C++ (gcc/g++ su Linux, Xcode su macOS)
- dlib
- OpenCV

---

## 🐧 Installazione su Linux (Ubuntu/Debian)

### 1. Installa le dipendenze di sistema

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv \
    cmake build-essential \
    libopencv-dev python3-opencv \
    libboost-all-dev \
    libx11-dev libgtk-3-dev
```

### 2. Crea un ambiente virtuale (consigliato)

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Installa le dipendenze Python

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Verifica l'installazione

```bash
python video2faces.py --help
```

---

## 🪟 Installazione su Windows con WSL

### 1. Installa WSL2 (se non già installato)

Apri PowerShell come amministratore:

```powershell
wsl --install
```

Riavvia il computer e completa la configurazione di Ubuntu.

### 2. Aggiorna WSL e installa le dipendenze

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv \
    cmake build-essential \
    libopencv-dev python3-opencv \
    libboost-all-dev \
    libx11-dev libgtk-3-dev
```

### 3. Configura la visualizzazione grafica (opzionale)

Per visualizzare la finestra video in WSL2, installa un X server su Windows (es. [VcXsrv](https://sourceforge.net/projects/vcxsrv/) o [X410](https://x410.dev/)):

```bash
# Aggiungi al tuo ~/.bashrc
export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0
export LIBGL_ALWAYS_INDIRECT=1
```

Oppure usa l'opzione `--no-display` per elaborazione senza GUI.

### 4. Crea ambiente virtuale e installa

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Accedi ai file Windows

I tuoi file Windows sono accessibili in `/mnt/c/Users/TuoNome/`:

```bash
python video2faces.py -i /mnt/c/Users/TuoNome/Videos/video.mp4
```

---

## 🍎 Installazione su macOS con Homebrew

### 1. Installa Homebrew (se non già installato)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. Installa le dipendenze di sistema

```bash
brew update
brew install python@3.11 cmake boost opencv
```

### 3. Crea un ambiente virtuale

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Installa le dipendenze Python

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Nota per Apple Silicon (M1/M2/M3)

Su Mac con chip Apple Silicon, potrebbe essere necessario:

```bash
# Installa Rosetta 2 se necessario
softwareupdate --install-rosetta

# Oppure compila dlib per ARM
pip install dlib --no-cache-dir --compile
```

Se riscontri problemi con face_recognition:

```bash
brew install openblas
export OPENBLAS=$(brew --prefix openblas)
pip install dlib --no-cache-dir
pip install face_recognition
```

---

## 🚀 Utilizzo

### Sintassi base

```bash
python video2faces.py -i <video_input> [opzioni]
```

### Esempi

```bash
# Elaborazione base (output in directory con timestamp)
python video2faces.py -i video.mp4

# Specifica directory di output
python video2faces.py -i video.mp4 -o ./output_analisi

# Elaborazione veloce (1 frame ogni 5, modello HOG)
python video2faces.py -i video.mp4 --skip-frames 5 --model hog

# Massima accuratezza
python video2faces.py -i video.mp4 --model cnn --upsample 2

# Elaborazione batch senza GUI
python video2faces.py -i video.mp4 --no-display

# Salva frame con rettangoli sui volti
python video2faces.py -i video.mp4 -t
```

### Opzioni disponibili

| Opzione | Descrizione | Default |
|---------|-------------|---------|
| `-i, --input` | File video di input (obbligatorio) | - |
| `-o, --output` | Directory di output | Timestamp corrente |
| `--skip-frames N` | Elabora 1 frame ogni N | 1 (tutti) |
| `--model` | Modello: `cnn` (accurato) o `hog` (veloce) | cnn |
| `--upsample N` | Upsampling per volti piccoli | 1 |
| `--no-display` | Disabilita visualizzazione live | False |
| `-t, --tag` | Disegna rettangoli verdi sui volti | False |

### Struttura output

```
2026_01_19_15_30_45/
├── volti/                          # Ritagli dei singoli volti
│   ├── 00_01_23_000150_face00.png
│   ├── 00_01_23_000150_face01.png
│   └── ...
├── frame/                          # Frame completi
│   ├── 00_01_23_000150.png
│   └── ...
└── report.html                     # Report interattivo
```

---

## ⚡ Ottimizzazione delle prestazioni

### Tabella prestazioni stimate

| Modello | Hardware | Tempo per frame |
|---------|----------|-----------------|
| CNN | GPU NVIDIA | ~0.05-0.1s |
| CNN | CPU | ~1-3s |
| HOG | CPU | ~0.1-0.3s |

### Suggerimenti

1. **Per analisi rapida**: usa `--model hog --skip-frames 5`
2. **Per massima accuratezza**: usa `--model cnn --upsample 2`
3. **Per elaborazione batch**: usa `--no-display`
4. **Con GPU NVIDIA**: installa CUDA e cuDNN per accelerazione CNN

### Supporto GPU (opzionale)

Per sfruttare la GPU NVIDIA:

```bash
# Installa CUDA toolkit
# Poi reinstalla dlib con supporto CUDA
pip uninstall dlib
pip install dlib --no-cache-dir
```

---

## 🔧 Risoluzione problemi

### "No module named 'face_recognition'"

```bash
pip install face_recognition
```

### "dlib not found" o errori di compilazione

```bash
# Linux
sudo apt install cmake build-essential libboost-all-dev

# macOS
brew install cmake boost

# Poi reinstalla
pip install dlib --no-cache-dir
```

### "Cannot open display" su WSL

Usa l'opzione `--no-display` oppure configura un X server.

### Memoria insufficiente con video lunghi

Usa `--skip-frames` per ridurre i frame elaborati:

```bash
python video2faces.py -i video_lungo.mp4 --skip-frames 10
```

### Volti non rilevati

- Prova ad aumentare `--upsample 2` per volti piccoli/lontani
- Usa `--model cnn` per maggiore accuratezza
- Verifica che i volti siano frontali e ben illuminati

---

## 📄 Licenza

Questo progetto è rilasciato sotto licenza MIT. Vedi il file [LICENSE](LICENSE) per i dettagli.

Utilizza la libreria [face_recognition](https://github.com/ageitgey/face_recognition) di Adam Geitgey, anch'essa sotto licenza MIT.

---

## 👤 Autore

**Antonio 'Visi@n' Broi**
- 🌐 [Tsurugi Linux](https://tsurugi-linux.org)
- 📧 antonio@tsurugi-linux.org

---

## 🙏 Ringraziamenti

- [face_recognition](https://github.com/ageitgey/face_recognition) - Adam Geitgey
- [dlib](http://dlib.net/) - Davis King
- [OpenCV](https://opencv.org/) - OpenCV Team
- [Tsurugi Linux](https://tsurugi-linux.org) - Digital Forensics Linux Distribution

---

## 📝 Changelog

### v2.0.0 (2026)
- ✨ Aggiunta generazione report HTML
- ✨ Naming convention con timestamp video
- ✨ Opzione `--tag` per rettangoli sui volti
- ✨ Directory output con timestamp data/ora
- ✨ Opzioni `--skip-frames`, `--model`, `--upsample`
- ✨ Modalità `--no-display` per elaborazione batch
- 🐛 Miglioramenti stabilità e gestione errori

### v1.0.0 (2022)
- 🎉 Release iniziale
