# Cross-Lingual TTS for Indian Languages: A Benchmark and Inference-Time Duration Estimation Strategies  

[![Paper](https://img.shields.io/badge/arXiv-2409.05356-brightgreen.svg?style=flat-square)]()
[![Demo](https://img.shields.io/badge/GitHub-Demo%20Page-orange.svg)](https://cross-lingual-tts-for-indian-languages.github.io/Cross-Lingual-TTS-Demo/)

### Our paper has been accepted to the AACL-IJCNLP 2026 Workshop Multi-LLL 
 
**Recipe for Preparing Cross-Lingual and Cross-Utterance Evaluation Test Sets**

This repository provides scripts for preparing **cross-lingual** and **cross-utterance (monolingual)** evaluation test sets for Text-to-Speech (TTS) systems.

The **cross-lingual evaluation protocol** follows the methodology proposed in our paper:



In addition, this repository includes a script for generating **cross-utterance (monolingual)** evaluation sets using the same data format, which can be used to benchmark zero-shot or voice-cloning TTS systems.

## Supported Languages

The repository currently provides evaluation test sets for:

- Telugu, Tamil, Hindi, Kannada, Malayalam, Punjabi, Odia, Marathi, Bengali, English
 
---

# Dataset Preparation

The evaluation sets are constructed from the following publicly available datasets.

### 1. Rasa Dataset

Download Test Split from:

https://huggingface.co/datasets/ai4bharat/Rasa

### 1. Indic Voices-R Dataset

Download Test Split from:

https://huggingface.co/datasets/ai4bharat/indicvoices_r


### 3. IndicTTS V2

Download Train Split from:

https://www.iitm.ac.in/donlab/indictts/

Please follow the original dataset licenses and usage terms.

---

# Repository Structure

```
cross_lingual/
│
├── telugu_english/
├── tamil_english/
├── hindi_english/
├── kannada_english/
├── malayalam_english/
├── punjabi_english/
├── odia_english/
├── marathi_english/
├── bengali_english/
└── english/
```

Each language directory contains

```
test_set_wav.scp
test_set.lst
```

---

# Test Set Format

## test_set_wav.scp

Maps utterance IDs to audio paths.

```
utterance_id    /path/to/audio.wav
```

---

## test_set.lst

Each line contains one evaluation pair.

```
reference_utterance   reference_duration  reference_text  generation_utterance  generation_duration  generation_text
```

Example

```
ENG_0012    5.32    Good morning everyone.   TEL_0234    6.71    ఆ నాడు సరికొత్తగా దివ్యదర్శనం ఇస్తున్నట్లనిపించింది అందరికీ.
```

where

- Reference utterance duration: **4–7 seconds**
- Generation utterance duration: **4–10 seconds**

## Cross-Lingual Evaluation Protocol

Each evaluation test set contains approximately **2 hours** of paired speech:

| Direction | Duration |
|-----------|----------|
| English Reference → Indian Language Generation | ~1 hour |
| Indian Language Reference → English Generation | ~1 hour |
| **Total** | **~2 hours** |

Reference utterances are **4–7 seconds**, while generation utterances are **4–10 seconds**. The dataset statistics follow those reported in the paper.

## Preparing a New Cross-Lingual Evaluation Set

Run:

```bash
python cross_lingual_prepare.py
```

Update the following parameters:

```python
GEN_TARGET_SECONDS = 3600      # 1 hour per language
data_folder = ""               # Indian language dataset
english = ""                   # English dataset
out_dir = "./{lang}_english"   # Output directory
```

## Required Dataset Format

Each language directory must contain the following files:

| File | Format |
|------|--------|
| `wav.scp` | `utterance_id    wav_path` |
| `utt2dur` | `utterance_id    duration` |
| `text` | `utterance_id    transcription` |

## Preparing a Cross-Utterance (Monolingual) Evaluation Set

Run:

```bash
python mono_lingual.py
```

Update the following parameters:

```python
GEN_TARGET_SECONDS = 7200      # 2-hour evaluation set
data_dir = "./input_folder"    # Directory containing: wav.scp, utt2dur, and text
out_dir = "./output_folder"    # Output directory
```

The script generates:

```
test_set_wav.scp
test_set.lst
```

Each entry in `test_set.lst` has the format:

```
reference_utterance  reference_duration  reference_text  generation_utterance  generation_duration  generation_text
```

Example:

```
TEL_0235  5.05  ఎక్కువ రేటింగ్ ఉన్న చైనీస్ క్యారిఔట్ మెనుకి నన్ను డైరెక్ట్ చెయ్యి..  TEL_0234  6.71  ఆ నాడు సరికొత్తగా దివ్యదర్శనం ఇస్తున్నట్లనిపించింది అందరికీ.
```

---
## Training Framework

Our experiments are built upon **A-DMA**, which extends the **F5-TTS** architecture for multilingual speech synthesis.

- **A-DMA:** https://github.com/ZhikangNiu/A-DMA
- **F5-TTS:** https://github.com/SWivid/F5-TTS

We thank the authors for making their implementations publicly available.

## Contact

For questions, suggestions, or issues regarding the evaluation protocol, please open a GitHub issue or contact:

**Arigala Adarsh**  
📧 arigalaadarsh780@gmail.com
