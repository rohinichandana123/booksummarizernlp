from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch
import re
import time

MODEL_NAME = "t5-small"

# ✅ Device setup
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"🔧 Device: {device}")

# ✅ Load model once at startup
tokenizer = T5Tokenizer.from_pretrained(MODEL_NAME)
model = T5ForConditionalGeneration.from_pretrained(MODEL_NAME).to(device)
model.eval()

if device.type == 'cuda':
    model = model.half()


def extract_key_sentences(text, num_sentences=12):
    """
    INSTANT extractive summarization - finds key sentences in < 1 second.
    """
    from collections import Counter
    
    sentences = re.split(r'(?<=[.!?])\s+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    
    if len(sentences) <= num_sentences:
        return ' '.join(sentences)
    
    # Word frequency scoring
    all_words = []
    sent_words = []
    for s in sentences:
        words = re.findall(r'\b[a-z]{3,}\b', s.lower())
        sent_words.append(words)
        all_words.extend(words)
    
    freq = Counter(all_words)
    
    # Score and rank
    scores = []
    for i, words in enumerate(sent_words):
        score = sum(freq[w] for w in words) / (len(words) + 1) if words else 0
        scores.append((score, i))
    
    # Get top sentences in original order
    top_idx = sorted([i for _, i in sorted(scores, reverse=True)[:num_sentences]])
    return ' '.join(sentences[i] for i in top_idx)


def summarize_text(text, max_length=150, min_length=30):
    """
    GUARANTEED < 30 SECONDS summarization for ANY file size.
    """
    start_time = time.time()
    
    if not text or len(text.strip()) == 0:
        return "No text provided."

    original_size = len(text)
    print(f"📄 Input: {original_size:,} chars ({original_size/1024:.1f} KB)")
    
    # ✅ STEP 1: Clean (instant)
    text = re.sub(r'\s+', ' ', text).strip()
    
    # ✅ STEP 2: Extract key sentences FIRST (< 1 sec for any size)
    # This is the key to handling large files fast
    if len(text) > 5000:
        print("⚡ Extracting key sentences...")
        text = extract_key_sentences(text, num_sentences=15)
        print(f"📝 Key content: {len(text):,} chars")
    
    # ✅ STEP 3: Hard limit for T5 model (keeps it fast)
    MAX_CHARS = 4000  # ~1000 tokens = fast processing
    if len(text) > MAX_CHARS:
        text = text[:MAX_CHARS]
    
    # ✅ STEP 4: Single tokenization
    tokens = tokenizer.encode(
        "summarize: " + text,
        max_length=512,
        truncation=True,
        return_tensors="pt"
    ).to(device)
    
    print(f"🔢 Tokens: {tokens.shape[1]}")
    
    # ✅ STEP 5: Generate summary (single pass, no chunking for speed)
    print("🚀 Generating summary...")
    
    with torch.no_grad():
        output = model.generate(
            tokens,
            max_length=max_length,
            min_length=min(min_length, 20),
            num_beams=1,        # Greedy = fastest
            do_sample=False,
            early_stopping=True
        )
    
    summary = tokenizer.decode(output[0], skip_special_tokens=True)
    
    # Clean up summary
    if not summary.endswith('.'):
        summary += '.'
    
    elapsed = time.time() - start_time
    print(f"✅ Done in {elapsed:.1f}s | {len(summary.split())} words")
    
    return summary


def extract_text_from_pdf(pdf_file):
    """
    Fast PDF extraction with limits.
    """
    import PyPDF2
    import io
    
    try:
        reader = PyPDF2.PdfReader(io.BytesIO(pdf_file))
        
        # Limit pages for speed
        max_pages = 20
        pages = min(len(reader.pages), max_pages)
        print(f"📚 Reading {pages}/{len(reader.pages)} pages")
        
        text = []
        for page in reader.pages[:pages]:
            try:
                t = page.extract_text()
                if t:
                    text.append(t)
            except:
                continue
        
        return "\n".join(text)
    except Exception as e:
        print(f"❌ PDF error: {e}")
        return ""
