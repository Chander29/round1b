import os
import json
import datetime
import re
from pdf_parser import PDFProcessor
from sentence_transformers import SentenceTransformer, util
from transformers import T5ForConditionalGeneration, T5Tokenizer

# Define paths
MODEL_PATH = 'models'
SUMMARIZER_PATH = 'models/summarizer'

def clean_text(text):
    text = text.replace('\ufb00', 'ff').replace('\ufb01', 'fi').replace('\ufb02', 'fl')
    text = text.replace('\u2022', '-').replace('\u2013', '-')
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def summarize_text(text, model, tokenizer):
    """
    Generates a concise summary of the given text.
    """
    # Prepare the text for T5
    t5_input_text = "summarize: " + text
    inputs = tokenizer.encode(t5_input_text, return_tensors="pt", max_length=1024, truncation=True)
    
    # Generate summary
    summary_ids = model.generate(inputs, max_length=150, min_length=50, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

def process_document_collection(test_case_dir, documents_list):
    all_sections = []
    for doc_info in documents_list:
        filename = doc_info['filename']
        file_path = os.path.join(test_case_dir, filename)
        try:
            processor = PDFProcessor(file_path)
            doc_sections = processor.get_sections()
            for section in doc_sections:
                section['document'] = filename
            all_sections.extend(doc_sections)
        except Exception as e:
            print(f"Error parsing {filename}: {e}")
    return all_sections

def find_relevant_sections(query, sections, model):
    if not sections: return []
    corpus = [f"{s['title']}: {clean_text(s['text'])}" for s in sections]
    corpus_embeddings = model.encode(corpus, convert_to_tensor=True, show_progress_bar=False)
    query_embedding = model.encode(query, convert_to_tensor=True)
    cosine_scores = util.cos_sim(query_embedding, corpus_embeddings)[0]
    for i, section in enumerate(sections):
        section['relevance_score'] = cosine_scores[i].item()
    sections.sort(key=lambda x: x['relevance_score'], reverse=True)
    return sections

def generate_output_json(ranked_sections, input_docs, persona, job, output_dir, summarizer, tokenizer):
    timestamp = datetime.datetime.now().isoformat()
    input_doc_names = [doc['filename'] for doc in input_docs]

    extracted_sections = []
    for i, section in enumerate(ranked_sections[:5]): # Limit to top 5 for performance
        extracted_sections.append({
            "document": section['document'],
            "section_title": section['title'],
            "importance_rank": i + 1,
            "page_number": section['page']
        })

    sub_section_analysis = []
    for section in ranked_sections[:5]:
        cleaned_content = clean_text(section['text'])
        # Generate a real summary
        summary = summarize_text(cleaned_content, summarizer, tokenizer)
        sub_section_analysis.append({
            "document": section['document'],
            "refined_text": summary,
            "page_number": section['page']
        })

    output_data = {
        "metadata": { "input_documents": input_doc_names, "persona": persona, "job_to_be_done": job, "processing_timestamp": timestamp },
        "extracted_sections": extracted_sections,
        "subsection_analysis": sub_section_analysis
    }

    output_path = os.path.join(output_dir, "challenge1b_output.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2)
    print(f"\nSuccessfully created final output at: {output_path}")

def main():
    test_case_dir = "input/test_case_1"
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    with open(os.path.join(test_case_dir, "input.json"), 'r') as f:
        input_data = json.load(f)
    
    documents_to_process = input_data['documents']
    persona = input_data['persona']['role']
    job = input_data['job_to_be_done']['task']
    smart_query = f"As a {persona}, I need to {job}"

    print("Loading models...")
    embedding_model = SentenceTransformer(MODEL_PATH)
    summarizer_model = T5ForConditionalGeneration.from_pretrained(SUMMARIZER_PATH)
    summarizer_tokenizer = T5Tokenizer.from_pretrained(SUMMARIZER_PATH)
    print("Models loaded.")

    sections = process_document_collection(test_case_dir, documents_to_process)
    if not sections: return

    ranked_sections = find_relevant_sections(smart_query, sections, embedding_model)
    generate_output_json(ranked_sections, documents_to_process, persona, job, output_dir, summarizer_model, summarizer_tokenizer)

if __name__ == "__main__":
    main()
