Approach Explanation: Persona-Driven Document Intelligence
Our solution is designed as an offline, model-driven system that acts as an intelligent document analyst. It identifies and ranks the most relevant sections from a collection of PDFs based on a user's persona and their specific job-to-be-done. The core of our approach is built on modern semantic search and summarization techniques, ensuring the system can understand the meaning and context of text without needing an internet connection.

Our methodology is broken down into four key stages:

1. Intelligent PDF Section Parsing
The first step is to deconstruct the provided PDF documents into manageable, content-rich sections. For this, we built a robust, heuristic-based parser. This module analyzes the typography and layout of each document to identify headings based on font size and style. It then intelligently groups all subsequent text under that heading until a new heading is found. This allows us to accurately segment a wide variety of documents, from structured reports to more stylistic brochures, into meaningful sections (e.g., "Coastal Adventures," "Culinary Experiences").

2. Semantic Query Formulation
To accurately understand the user's intent, we create a "smart query" by combining the provided Persona and Job-to-be-Done into a single, context-rich sentence. For example, "As a PhD Researcher in Computational Biology, I need to prepare a comprehensive literature review..." This provides the AI model with a much clearer picture of the user's goal than either piece of information would alone.

3. Offline Semantic Search and Summarization
This is the core of our intelligent system, using two distinct offline models:

Semantic Ranking: We use a compact and powerful sentence-transformer model (all-MiniLM-L6-v2) to convert our smart query and every document section into numerical vectors ("embeddings"). By calculating the cosine similarity between the query's embedding and each section's embedding, we can mathematically determine which sections are most semantically relevant to the user's goal.

Text Summarization: For the subsection_analysis, we generate a true, concise summary of the most relevant sections. We use an offline t5-small model, a transformer-based model fine-tuned for summarization. This provides a human-readable summary of the key information in each section, rather than just a raw text snippet.

4. Ranking and Output Generation
The sections are sorted in descending order based on their relevance score. The top-ranked sections are then formatted into the required challenge1b_output.json structure, which includes the necessary metadata, a ranked list of the most important sections, and the AI-generated summaries for context.

This end-to-end, offline approach creates a powerful and generic document intelligence engine that is fast, accurate, and fully compliant with all hackathon constraints.