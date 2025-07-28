from sentence_transformers import SentenceTransformer
from transformers import T5ForConditionalGeneration, T5Tokenizer

# --- Download Embedding Model ---
embed_model_name = 'all-MiniLM-L6-v2'
embed_model_path = 'models'
print(f"Downloading embedding model '{embed_model_name}'...")
model = SentenceTransformer(embed_model_name)
model.save(embed_model_path)
print(f"Embedding model saved to '{embed_model_path}' directory.")

# --- Download Summarization Model ---
summary_model_name = 't5-small'
summary_model_path = 'models/summarizer'
print(f"Downloading summarization model '{summary_model_name}'...")
tokenizer = T5Tokenizer.from_pretrained(summary_model_name)
model = T5ForConditionalGeneration.from_pretrained(summary_model_name)
tokenizer.save_pretrained(summary_model_path)
model.save_pretrained(summary_model_path)
print(f"Summarization model saved to '{summary_model_path}' directory.")
