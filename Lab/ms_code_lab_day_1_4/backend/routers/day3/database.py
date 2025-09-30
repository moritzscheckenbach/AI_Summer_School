import os

from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from pypdf import PdfReader
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

data_dir = os.path.dirname("/home/moritz_s/Desktop/ai_summer_school/Code/summerschool-2025/data/")
pdf_dir = os.path.join(data_dir, "Owners_Manual_tesla.pdf")


def extract_pdf_content(pdf_path):
    reader = PdfReader(pdf_path)

    # Create a list of documents with simplified metadata
    documents = []
    for page_num, page in enumerate(reader.pages):
        text_content = page.extract_text()
        doc = Document(page_content=text_content, metadata={"doc_id": os.path.basename(pdf_path), "page_number": page_num + 1})
        documents.append(doc)

    return {"documents": documents, "num_pages": len(reader.pages)}


def chunk_documents(documents, chunk_size=1000, chunk_overlap=100):
    """
    Chunk documents into semantically meaningful sentences while preserving metadata
    Args:
        documents: List of Document objects
        chunk_size: Maximum size of each chunk
        chunk_overlap: Number of characters to overlap between chunks
    Returns:
        List of Document objects with sentence-based chunks
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=[". ", "? ", "! ", ".\n", "?\n", "!\n", "\n\n", "\n", " ", ""],
    )

    # Add chunk_id to metadata during splitting
    chunked_documents = text_splitter.split_documents(documents)
    for chunk_id, chunk in enumerate(chunked_documents):
        chunk.metadata["chunk_id"] = chunk_id

    print(f"Created {len(chunked_documents)} chunks")
    print(f"Sample chunk metadata: {chunked_documents[0].metadata}")

    return chunked_documents


def create_vector_store(chunks):
    """
    Create a vector store from document chunks
    Args:
        chunks: List of Document objects with content and metadata
    Returns:
        Qdrant vector store instance
    """
    # Initialize embedding model
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Initialize Qdrant client in memory
    client = QdrantClient(":memory:")

    # Get vector size from embedding model
    vector_size = len(embeddings.embed_query("test"))

    # Create collection if it doesn't exist
    if not client.collection_exists("tesla_manual"):
        client.create_collection(collection_name="tesla_manual", vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE))

    # Create vector store
    vector_store = QdrantVectorStore(
        client=client,
        collection_name="tesla_manual",
        embedding=embeddings,
    )

    # Add documents to vector store
    vector_store.add_documents(chunks)

    return vector_store


def main():
    # Extract and chunk content
    result = extract_pdf_content(pdf_dir)
    chunks = chunk_documents(result["documents"])

    # # Print some statistics and examples
    # print(f"Number of chunks: {len(chunks)}")
    # print(f"Average chunk length: {sum(len(doc.page_content) for doc in chunks)/len(chunks)}")
    # print(f"\nFirst chunk preview:")
    # print(f"Content: {chunks[0].page_content[:200]}...")
    # print(f"Metadata: {chunks[0].metadata}")
    # print(f"\nMiddle chunk (500):")
    # print(f"Content: {chunks[500].page_content[:200]}...")
    # print(f"Metadata: {chunks[500].metadata}")

    # Create vector store
    vector_store = create_vector_store(chunks)

    # Test similarity search
    query = "How do I charge the battery?"
    threshold = 0.21  # Adjust this threshold based on your needs
    all_docs = vector_store.similarity_search_with_score(query, k=4)

    for doc, score in all_docs:
        print("\n-------------------")
        print(f"Similarity Score: {score:.4f}")
        print(f"Content: {doc.page_content[:200]}...")
        print(f"Metadata: {doc.metadata}")

    # Filter documents by score while maintaining the (doc, score) tuple structure
    found_docs = [(doc, score) for doc, score in all_docs if score >= threshold]

    # Print filtered results
    if found_docs:
        for doc, score in found_docs:
            print("\n+++++++++++++++++++")
            print(f"Similarity Score: {score:.4f}")
            print(f"Content: {doc.page_content[:200]}...")
            print(f"Metadata: {doc.metadata}")
    else:
        print("\nNo documents found above the threshold score.")


if __name__ == "__main__":
    main()
