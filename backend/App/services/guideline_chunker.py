from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_guidelines(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
    )

    chunks = []

    for doc in documents:
        split_docs = splitter.create_documents(
            [doc["text"]],
            metadatas=[
                {
                    "file_name": doc["file_name"]
                }
            ],
        )

        chunks.extend(split_docs)

    return chunks