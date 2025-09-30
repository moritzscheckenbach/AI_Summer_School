# Day 3: Practical RAG Lab

## 🎯 What You Will Build

You'll create a minimal-but-solid RAG (Retrieval-Augmented Generation) system using a **Tesla Owner's Manual** as your knowledge base. The core pipeline will be:

1. **Ingest:** Load, chunk, embed, and index the document content.
2. **Retrieve & Generate:** Fetch relevant context, (optionally) re-rank it, and generate a concise answer with citations.
3. **Evaluate:** Use an **LLM-as-judge** to automatically score your RAG pipeline's performance against a provided test set.
4. **Expose:** Create a simple **`/chat`** API endpoint for live, interactive testing.

-----

## 🛠️ Constraints

* **Framework:** You **can** choose **one** of the following: **LangChain**, **LlamaIndex**, or **Haystack**. Or built from sratch using custom components.
* **Simplicity:** No complex setup is required. I recomment prioritize file-based vector stores to keep things simple.

-----

## 🗂️ Vector Database Options

You'll need a vector database to store your document embeddings. Here are some excellent choices that are easy to run and well-supported by the frameworks.

### No Server, `pip`-install only

These options are the simplest to get started with and are perfect for this lab.

* **FAISS:** A highly efficient similarity search library.
  * *Supported by: LangChain ✅, LlamaIndex ✅, Haystack ✅*
  * `pip install faiss-cpu`
* **Chroma:** A popular, open-source embedding database.
  * *Supported by: LangChain ✅, LlamaIndex ✅, Haystack ✅*
  * `pip install chromadb`
* **LanceDB:** A modern, serverless vector database built on an efficient columnar format.
  * *Supported by: LangChain ✅, LlamaIndex ✅*
  * `pip install lancedb`

### Lightweight Server (Optional)

If you're comfortable with Docker and want to try a more production-style setup, these are great options.

* **Qdrant:** A fast and scalable vector database.
  * *Supported by: LangChain ✅, LlamaIndex ✅, Haystack ✅*
  * `uv add qdrant-client`
  * **💡 Hint:** While the file-based options above are simpler for a quick start, **Qdrant is a very solid and recommended choice** if you want to experience a robust, client-server vector DB. It requires some basic Docker knowledge to run the server.

> **My Recommendation:** For a smooth start, begin with **FAISS** or **Chroma**. If you want a challenge and a more realistic setup, give **Qdrant** a try.

-----

## 🧠 Embedding Model Selection

The quality of your embeddings is critical to your RAG system's success. For this lab, you must select and compare at least **three different embedding models**.

Your goal is to understand the trade-offs between model size, performance, and resource usage. We encourage you to pick models with different dimensions (e.g., 384 vs. 768) or from different top-performing families.

The **Hugging Face MTEB (Massive Text Embedding Benchmark) Leaderboard** is the definitive resource for finding and comparing state-of-the-art models. Explore the leaderboard to make your selections. You can also compare a local open-weights model against a proprietary API like OpenAI's `text-embedding-3-small`.

#### Implementation

To easily integrate open-source models into your chosen framework, refer to their documentation.

* **Haystack:** [SentenceTransformersDocumentEmbedder](https://docs.haystack.deepset.ai/docs/sentencetransformersdocumentembedder)
* **LangChain:** [Sentence Transformers Integrations](https://python.langchain.com/docs/integrations/text_embedding/sentence_transformers/)

## ✅ Core Tasks

### Task 1: Ingestion & Indexing

Your first step is to process the source document and build your vector indexes.

* Load the provided Tesla manual PDF and extract its text and page numbers.
* Use an appropriate tool to parse the pdf.
* Ensure each chunk has essential metadata: **`doc_id`**, **`page_number`**, etc..

💡 **Hint:** PDF parsing is notoriously messy\! Raw text extraction can garble tables or include unwanted headers and footers. You may need to perform some pre-processing and cleaning on the extracted text *before* chunking to get good results.

**Deliverable:** A small summary table logging your experimental configurations: `(chunker_strategy, embedding_model, dimensions, index_type, build_time_seconds, num_chunks)`.

### Task 2: Retrieval

Now, build the retrieval component that will find context for the LLM.

* Implement a retrieval function that performs a similarity search over your index. It should be configurable for `k` (the number of chunks to retrieve).
* Add a threshold to identify irrelevant document.

**Deliverable:** A function that takes a query and returns the top-k chunks, including their content, scores, and metadata.

### Task 3: Generation

With retrieval in place, you can now generate answers.

* Create a prompt template that:
  * Clearly separates the user's **question** from the retrieved **context**.
  * Instructs the LLM to generate a concise answer based *only* on the provided context.
  * Requires the LLM to cite its sources using the metadata from the retrieved chunks: `[(doc_id, page_number, chunk_id)]`.
  * Explicitly forbids making up information and instructs the model to state when the answer is not found in the context.
* Add simple controls to your generation logic for **max answer length** and **temperature**.

**Deliverable:** A generation function that orchestrates the retrieval and LLM call to produce a final answer with citations.

### Task 4: LLM-as-Judge (Automatic Evaluation)

Finally, you'll evaluate your RAG pipeline automatically using another LLM.

* Use the provided JSON test set, which contains `{"question": "...", "answer": "..."}` pairs as the ground truth.
* For each question in the test set, run your full RAG pipeline to get a predicted answer.
* Create a "judge" prompt that asks a powerful LLM (e.g., GPT-4, Claude 3) to compare the predicted answer to the ground truth answer and score it on **Exactness**, **Groundedness**, and **Completeness**. The judge must output a structured JSON object.

⚠️ **A Word of Caution:** LLM-as-judge is a powerful but imperfect technique. Its judgments can be influenced by the specific judge model used and the wording of your evaluation prompt. For this lab, start with a small, representative test set (`~10-15 questions`) to keep evaluation time and API costs manageable.


**Deliverable:** A script that automates the evaluation process and outputs a summary of the average scores for each of your RAG configurations.


## Usable embedding models
| Model Name                  | MTEB Score* | Size          | Year/Status           | Hugging Face Repo                                                   |
|-----------------------------|-------------|---------------|-----------------------|---------------------------------------------------------------------|
| EmbeddingGemma              | 68.2        | 308M params   | 2025 / Released       | hhttps://huggingface.co/blog/embeddinggemma         |
| jina-embeddings-v3          | 65.5        | 570M params   | 2025 / Released       | https://huggingface.co/jinaai/jina-embeddings-v3               |
| Nomic Embed Text V2         | ~61–63      | —             | 2024 / Released       | https://huggingface.co/nomic-ai/nomic-embed-text-v2-moe                 |
| BAAI bge-m3                 | ~60–61      | 660M params   | 2024 / Released       | https://huggingface.co/BAAI/bge-m3                                  |
| Alibaba GTE-multilingual    | ~64–66      | 305M params   | 2024 / Released       | https://huggingface.co/Alibaba-NLP/gte-multilingual-base            |
| MiniLM Multilingual         | ~55–59      | 22–80M params | 2022+/Still used      | https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 |
