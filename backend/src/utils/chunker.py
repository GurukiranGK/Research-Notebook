from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_text(text: str) -> list[dict]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        separators=["\n\n", "\n", " ", ""],
    )
    docs = splitter.create_documents([text])
    return [{"content": doc.page_content, "order": index} for index, doc in enumerate(docs)]
