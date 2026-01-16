import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import ctranslate2
import transformers
import os
import time

# Options
MODEL_PATH = "nllb-200-distilled-600M-int8" # Path to the CTranslate2 model directory
TOKENIZER_ID = "facebook/nllb-200-distilled-600M" # HuggingFace ID for tokenizer

app = FastAPI()

print("Loading tokenizer...")
tokenizer = transformers.AutoTokenizer.from_pretrained(TOKENIZER_ID)

print(f"Loading CTranslate2 model from {MODEL_PATH}...")
# Check if model exists
if not os.path.exists(MODEL_PATH):
    print(f"WARNING: Model path '{MODEL_PATH}' not found.")
    print("Please download a converted model or convert one using ctranslate2-converter-transformers.")
    print("Example: ctranslate2-converter-transformers --model facebook/nllb-200-distilled-600M --output_dir nllb-200-distilled-600M-int8 --quantization int8")
    translator = None
else:
    # Robust loading with fallback
    try:
        print("Attempting to load model with device='auto'...")
        translator = ctranslate2.Translator(MODEL_PATH, device="auto")
        # Perform a warmup translation to trigger lazy loading of libraries (like cuBLAS)
        # using a simple token list and a target prefix
        translator.translate_batch([["test"]], target_prefix=[["eng_Latn"]])
        print(f"Model loaded successfully. Device: {translator.device}")
    except Exception as e:
        print(f"Error loading model with device='auto': {e}")
        print("Falling back to device='cpu'...")
        
        # Aggressively prevent partial CUDA loading by hiding devices
        os.environ["CUDA_VISIBLE_DEVICES"] = "" 
        
        # Clean up if possible
        if 'translator' in locals():
            try:
                del translator
            except:
                pass

        try:
            translator = ctranslate2.Translator(MODEL_PATH, device="cpu")
            translator.translate_batch([["test"]], target_prefix=[["eng_Latn"]])
            print("Model loaded successfully on CPU.")
        except Exception as e_cpu:
            print(f"CRITICAL: Failed to load model on CPU: {e_cpu}")
            translator = None

class TranslationRequest(BaseModel):
    text: str
    source_lang: str = "autodetect" # "eng_Latn", "zho_Hans", etc.
    target_lang: str = "zho_Hans"

# Simple mapping from common 2-letter codes to NLLB codes
# You can extend this map as needed
LANG_MAP = {
    "en": "eng_Latn",
    "zh": "zho_Hans",
    "zh-cn": "zho_Hans",
    "ja": "jpn_Jpan",
    "ko": "kor_Hang",
    "fr": "fra_Latn",
    "de": "deu_Latn",
    "es": "spa_Latn",
    "ru": "rus_Cyrl",
    "th": "tha_Thai",
    "vi": "vie_Latn",
    "it": "ita_Latn",
    "pt": "por_Latn",
    "hi": "hin_Deva",
    # Add more mappings as needed
}

def map_lang(code: str) -> str:
    code = code.lower()
    if code in LANG_MAP:
        return LANG_MAP[code]
    # If not in map, assume it might be a full NLLB code or pass through
    # NLLB codes usually look like 'xxx_Script'
    return code

@app.get("/")
def read_root():
    return {"status": "ok", "message": "NLLB Translation Server is running. Use POST /translate to translate text."}

@app.get("/translate")
def read_translate_get():
    return {"status": "error", "message": "This endpoint requires a POST request via JSON. Please use the application or a tool like Postman."}

@app.post("/translate")
async def translate(req: TranslationRequest):
    if translator is None:
        raise HTTPException(status_code=500, detail="Model not loaded. Please check server logs.")

    start_time = time.time()
    
    source_lang = map_lang(req.source_lang)
    target_lang = map_lang(req.target_lang)

    # Note: NLLB requires source language for tokenization usually, 
    # but CTranslate2 often handles it via properties or special tokens depending on conversion.
    # For NLLB tokenizer, we explicitly set src_lang.
    
    if source_lang == "autodetect":
        # Fallback or implement detection. For now default to English if unknown
        source_lang = "eng_Latn" 

    try:
        # Tokenize
        tokenizer.src_lang = source_lang
        source = tokenizer.convert_ids_to_tokens(tokenizer.encode(req.text))

        # Translate
        results = translator.translate_batch(
            [source], 
            target_prefix=[[target_lang]]
        )
        
        target = results[0].hypotheses[0]
        translated_text = tokenizer.decode(tokenizer.convert_tokens_to_ids(target), skip_special_tokens=True)

        print(f"[{time.time() - start_time:.3f}s] {source_lang}->{target_lang}: {len(req.text)} chars")
        
        return {"translation": translated_text}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Translation Error: {str(e)}")

if __name__ == "__main__":
    print("Starting NLLB Server on port 8000...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
