# Chapter 65: Low-Resource Language Analytics — Kumba and the Languages the Internet Forgot

*Part XI — The Frontier: Advanced Methods and Emerging Practice*

> "The models were trained on the internet's languages; your customers were not born on the internet."

### In this chapter you will learn

- What "low-resource" means, and why Shona and Ndebele analytics underperform English — by construction.
- Tokenisation and subword vocabularies: why SentencePiece beats word-level for agglutinative languages.
- Transfer learning: borrowing structure from high-resource neighbours.
- The evaluation set you must build by hand — and why it becomes the moat.
- Kumba's stack: transcription, search, and moderation in-language.
- Ethics: data sovereignty, consent, and who owns a corpus.

## 65.1 The Problem

**Kumba** (Chapter 60's media company) streams news and radio in Shona and Ndebele to an audience the internet's tools barely see. Off-the-shelf speech recognition mangles Shona names; search works only for users who type English queries; sentiment models return confident nonsense. The reason is not magic: modern language tools are statistical reflections of their training data, and the internet holds perhaps a thousand times more English than Shona. Low-resource does not mean the language is poor in structure — it means the *data infrastructure* is thin: few corpora, few annotators, few benchmarks, few tools that ship with the language preloaded.

The strategic framing every analyst should internalise: **where the tooling is thin, the data you can build becomes the moat.** Kumba's competitive asset is not a model; it is ten thousand hours of transcribed Shona audio and the eval sets no competitor owns.

## 65.2 Tokenisation: Words Are Not the Unit

English tokenisation (split on spaces) fails hard on agglutinative languages, where one word carries what English spends a sentence on — a Shona verb absorbs subject, tense, object, and mood into a single token. A word-level vocabulary explodes into millions of mostly-unseen entries. The fix is **subword tokenisation**: learn a vocabulary of frequent pieces (SentencePiece, BPE) sized to the corpus, so every unseen word decomposes into known parts.

```python
import sentencepiece as spm
spm.SentencePieceTrainer.train(
    input="shona_corpus.txt", model_prefix="shona_sp",
    vocab_size=8000, model_type="bpe",
    character_coverage=1.0)          # every character must be reachable
sp = spm.SentencePieceProcessor(model_file="shona_sp.model")
print(sp.encode("ndakamuida muno", out_type=str))
# ['▁nda', 'ka', 'mu', 'ida', '▁muno']  — morphemes, not words
```

The craft decisions: vocabulary size matched to corpus size (8k for a million lines, not 50k), `character_coverage=1.0` so diacritics never become unknowns, and **one tokeniser per language** — a Shona-Ndebele hybrid vocabulary serves neither.

## 65.3 Transfer: Borrowing Structure

You cannot train a large language model from scratch on thin data — but you do not have to. The transfer ladder, cheapest first:

1. **Continue-pretraining** an existing multilingual model on your corpus (further pretraining on Shona text).
2. **Fine-tune** on a small labelled task set (classification, tagging) with aggressive regularisation and early stopping.
3. **Adapters / parameter-efficient tuning** — freeze the base, train a small inserted module; hundreds of thousands of parameters instead of hundreds of millions, which is what a labelled set of 3,000 sentences can actually support.
4. **Related-language transfer** — structure learned on languages with larger corpora and shared roots moves better than structure learned on unrelated giants.

The honesty clause: transfer raises the floor but does not close the gap, and the gap is measurable — which is Section 65.4's entire point.

## 65.4 The Evaluation Set You Build By Hand

No benchmark exists, so you construct one: 500 sentences annotated for the task (intent, sentiment, named entities), stratified across dialects, registers (radio Shona, street Shona, formal news), and the hard cases (code-switching — the sentence that drifts into English mid-thought — which is not noise but the *dominant register* of real usage).

The discipline that makes it a moat rather than a chore: annotate twice (two speakers, adjudicated disagreements), freeze the set, never train on it, and score every model change against it. **The eval set is the product**: models are replaceable, the measurement instrument is not. When Kumba's transcription vendor claims "30% better", the claim dies or survives on the frozen set — and the set improves only by deliberate, versioned additions.

## 65.5 Kumba's Stack

- **Transcription**: a fine-tuned speech model on ten thousand labelled minutes; the eval set is 200 hand-checked hours covering accents, music beds, and code-switching. Word error rate on the eval set, published internally every release.
- **Search**: the untitled archive (Chapter 60) titled in-language — subword tokenisation means a query matches across morphological variants; embeddings fine-tuned on listener behaviour so "murimi" finds the farming programme the listener cannot name.
- **Moderation**: comment and call-in triage in-language — the English model's confidence was the danger (confident nonsense, silently applied); the fine-tuned model is calibrated to admit what it cannot read.

**From Your Toolkit — Python:** this is the one frontier where only Python reaches — your SQL moves the data, your Power BI monitors the pipelines, but the language work is a Python notebook discipline, end to end. The six-tool grammar holds: the new tool implements an old idea — representation, learned from data — and the bridge names it.

## 65.6 Ethics: Whose Corpus Is It?

The corpus is communities' speech, gathered under consent that must be specific and revocable; the annotators are speakers whose expertise deserves more than piecework rates; and the models built on a community's language should be auditable by that community. Data sovereignty in practice: provenance recorded per item (Chapter 42's lineage, applied to audio), opt-out honoured by retraining, and the eval sets documented so the community's dialects are visible in the measurement, not averaged into the standard register.

## 65.7 Failure Modes

- **The English benchmark halo** — "our model is state of the art" on an English-adjacent eval, deployed on Shona; the only number that matters is the one on your frozen set.
- **Tokeniser mismatch** — training data tokenised one way, serving traffic another; the vocabulary must version with the model, together.
- **The code-switching blind spot** — models trained on "pure" text meet real speech mid-drift; stratify the eval set for it or miss the dominant register.
- **Confident nonsense** — the calibrated-to-English confidence scores applied in-language; recalibrate on the in-language eval set before any automated decision.

> **Teaching Tip — The untranslated search box:** put a search interface in front of the class and have Shona-speaking students query it while everyone watches the results. Two minutes of watching real queries fail — then succeed after subword tokenisation — teaches the whole chapter's motivation with no slides at all. Students who have watched a language be ignored by software never forget whose problem this is.

## Key Takeaways

- Low-resource is a data-infrastructure condition, not a property of the language — and the corpus you build is the moat.
- Subword tokenisation (one per language, character coverage 1.0) replaces the word-level vocabulary that explodes.
- Transfer the structure (continue-pretrain, fine-tune, adapters), then measure the remaining gap — do not claim it closed.
- The hand-built, frozen, dual-annotated evaluation set is the product; every claim dies or survives on it.
- Consent, provenance, and community auditability are the ethics floor for speech corpora.

## Practice Lab

1. Train a SentencePiece model on a Shona (or any low-resource) corpus at two vocabulary sizes; measure out-of-vocabulary rate on held-out text and justify your chosen size.
2. Fine-tune a multilingual model on a 2,000-sentence sentiment task; evaluate on the frozen hand-built set and report the gap to its English performance honestly.
3. Build the eval set: 200 sentences, two annotators, adjudication log, stratification across registers including code-switching; write the versioned documentation page.
4. The search audit: index the archive with word-level and subword tokenisation; run 20 real listener queries against both; report the recall difference.
5. The calibration fix: take the English-calibrated confidence scores, recalibrate on your in-language set, and show the decision-threshold difference it causes.
6. The sovereignty memo: for a corpus of community speech, write the provenance, consent, and opt-out plan — and the paragraph you would show the community's elders.

## Further Reading

- Masakhane's published papers (the reference community for African-language NLP)
- *Natural Language Processing with Transformers* — Tunstall, von Wille and Wolf (free online)
- Chapter 60 (Kumba's media business), Chapter 42 (lineage for corpora), Chapter 68 (privacy, when the data is people's voices)
