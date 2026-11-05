# Survival AI (IA da Sobrevivência)

**A survival assistant that works 100% without internet** — on Windows, Linux and macOS.

[🇧🇷 Português](README.md) · 🇺🇸 English · [🇪🇸 Español](README.es.md)

If the internet, power and services go down, this kit keeps working on a laptop or USB drive:

- 📚 **Practical guides with cited sources** (EN, PT, ES): water, fire, shelter, food, gardening and livestock, foraging/fishing/hunting, **first aid and medicine**, hygiene and homemade soap, **alcohol** (fermentation, distillation, antiseptic and fuel), solar power, radio and navigation, tools and knots, mental health and community, and checklists for 72 hours and **1 year**.
- 🤖 **Local AI** that answers any question in natural language, **citing its sources** — it runs on your own computer (llama.cpp or Ollama); nothing goes to the internet.
- 🌐 **Kiwix offline libraries**: medical Wikipedia, post-disaster manuals, *Where There Is No Doctor*, wikiHow, iFixit and more — the AI searches them too.
- 📱 **Web interface** in your browser, shareable over the local network (other phones connect via Wi-Fi, even with no internet).
- 🔍 **No-AI mode**: even without a model, guide search works on any PC with Python.

> ⚠️ **Disclaimer:** educational content. It does not replace doctors, firefighters or emergency services. Health guidance follows public guidelines (WHO, Red Cross/IFRC, AHA, CDC, Hesperian…) cited in each section.

---

## How it works

```
 Question ──► search kit guides (BM25) ──────┐
          └─► search Kiwix (.zim files) ──────┼─► local language model ──► answer with [1] [2] sources
                                              └─► (no model? shows the most relevant passages)
```

| Part | What it is | Where |
|---|---|---|
| `sobrevivencia.py` + `app/` | The AI (Python standard library only, no `pip install`) | repository |
| `knowledge/pt|en|es/` | Survival guides in Markdown | repository |
| `knowledge/extra/` | **Your** `.md`/`.txt` documents (searched and cited by the AI) | repository |
| `runtime/llama.cpp/` | Engine that runs the AI model | downloaded by the preparer |
| `models/*.gguf` | Language model (1–5 GB) | downloaded by the preparer |
| `runtime/kiwix-tools/` + `zim/*.zim` | Kiwix server and libraries | downloaded by the preparer |
| `runtime/python/` | Portable Python (for PCs without Python) | downloaded by the preparer |

Large files are **not committed to git** (see `.gitignore`): the repository stays small and everyone builds their own kit with the preparer.

---

## Quick start

### 1. Get the repository

```bash
git clone https://github.com/sdalberto/ia-da-sobrevivencia.git
cd ia-da-sobrevivencia
```

### 2. Prepare the kit (online, once)

| System | How to run |
|---|---|
| **Windows** | double-click `preparar-kit.bat` |
| **macOS** | double-click `preparar-kit.command` (first time: right-click › Open) |
| **Linux** | `./preparar-kit.sh --lang en` |

The preparer asks for:

1. **AI model:** `leve` (light, 1 GB, 4 GB RAM), `padrao` (default, 2 GB, 8 GB RAM — recommended), `forte` (strong, 4.7 GB, 16 GB RAM).
2. **Kiwix libraries:** `minimo` (~3–5 GB), `recomendado` (~25–40 GB) or `completo` (100+ GB, full Wikipedia).
3. **Systems:** this computer only, or **Windows + Linux + macOS** (universal USB kit).
4. **Portable Python:** so the kit opens on computers without Python.

Non-interactive:

```bash
python sobrevivencia.py --lang en prepare --model padrao --zims recomendado --os all --python
```

### 3. Use it (offline)

| System | How to open |
|---|---|
| **Windows** | `iniciar.bat --lang en` (or double-click `iniciar.bat` and press **EN**) |
| **macOS** | `iniciar.command` |
| **Linux** | `./iniciar.sh --lang en` |

Your browser opens <http://127.0.0.1:8090>. Switch language anytime with the PT/EN/ES buttons. To make English the default, create `config/settings.local.json` with `{ "language": "en" }`.

### 4. Carry it on a USB drive

Copy **the whole folder** to a USB drive or external disk formatted as **exFAT** (works on all three systems and supports files over 4 GB).

---

## Other ways to use it

```bash
python sobrevivencia.py --lang en chat                   # terminal chat
python sobrevivencia.py --lang en ask "how do I make oral rehydration solution?"
python sobrevivencia.py --lang en search burn
python sobrevivencia.py status
python sobrevivencia.py start --host 0.0.0.0             # share on the local network
python sobrevivencia.py prepare --search survival        # find more Kiwix libraries
```

**Ollama:** if you use [Ollama](https://ollama.com), run `ollama pull qwen2.5:3b` — it is detected automatically. Any local OpenAI-compatible server (LM Studio, llamafile, KoboldCpp, Jan) also works: set `llm_url`.

**Kiwix Desktop:** [Kiwix Desktop](https://kiwix.org) can open the `.zim` files in `zim/`. To let the AI use its *Local Kiwix Server*, set `{ "kiwix_url": "http://127.0.0.1:<port>" }` in `config/settings.local.json`. The Windows Kiwix Desktop package (~150 MB) exceeds GitHub's 100 MB per-file limit — publish it as a **Release asset** instead of committing it.

## Add your own knowledge

Drop `.md` or `.txt` files in `knowledge/extra/` (family recipes, local maps, contacts, equipment manuals). They are indexed and cited by the AI.

## Requirements

- **Minimum (search only):** any PC with Python 3.8+.
- **With AI:** 4 GB RAM (light model), 8 GB recommended; x86-64 CPU with AVX2 or Apple Silicon/ARM64. No GPU needed.
- **Disk:** 3 GB (minimal kit) to 100+ GB (full kit).

## Tests

```bash
python -m unittest discover -s tests
```

## Licenses

Code: [MIT](LICENSE). Guides in `knowledge/`: [CC BY-SA 4.0](LICENSE-CONTENT.md). Models, Kiwix, llama.cpp and ZIM files downloaded by the preparer have their own licenses. The default model (Qwen2.5 3B) uses the *Qwen Research License*; for commercial use choose `leve` or `forte` (Apache 2.0).
