# Panic Level Feature (RoBERTa Fine-Tune)

This module contains the configuration and tokenizer files for the **Panic Level** detector — part of the G-Pattern signal family inside the DDS Hybrid Inference system.

## What It Does
This model estimates how much panic or emotional intensity shows up in a text sample.  
It helps flag phrases that sound alarmist or fear-driven, so the HP layer can weigh incident credibility more accurately.

## Model Snapshot
- Base: `roberta-base`
- Architecture: `RobertaForSequenceClassification` (binary)
- Hidden size: 768 Layers: 12 Heads: 12
- Dropout: 0.1 Max length: 512
- Task: `single_label_classification`

## Training Summary
| Setting | Value |
|----------|--------|
| Dataset sources | GoEmotions (fear/anger/surprise) + HateXplain (offensive/alarmist) |
| Epochs | 3 |
| Batch size | 16 |
| Learning rate | 2e-5 |
| Optimizer | AdamW |
| Final loss | Train ≈ 0.08 / Val ≈ 0.16 |

## Files in This Folder
| File | Role |
|------|------|
| `config.json` | Model architecture |
| `tokenizer_config.json` | Tokenizer parameters |
| `special_tokens_map.json` | Maps pad/cls/mask tokens |
| `merges.txt` | BPE merge rules |
| `vocab.json` | Token-ID mapping |
| `tokenizer.json` | Combined tokenizer definition |

> The full weight file (`model.safetensors`, ~500 MB) lives in Google Drive:  
> `/MyDrive/DDS_Models/panic_level_model/`  
> It’s not pushed to GitHub due to file-size limits.

## Quick Use
```python
from transformers import AutoModelForSequenceClassification, AutoTokenizer

model = AutoModelForSequenceClassification.from_pretrained(
    "/content/drive/MyDrive/DDS_Models/panic_level_model"
)
tokenizer = AutoTokenizer.from_pretrained(
    "/content/drive/MyDrive/DDS_Models/panic_level_model"
)
