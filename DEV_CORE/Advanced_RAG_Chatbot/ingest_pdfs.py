import os
import shutil
from config import Config



def process_pdfs():
    print("Function process_pdfs started.")
    # Source PDF directory (root DEV folder)
    base_dir = Config.BASE_DIR
    parent_dir = os.path.dirname(base_dir)
    src_dir = os.path.join(parent_dir, "DEV")
    
    print(f"Base Dir: {base_dir}")
    print(f"Source Dir: {src_dir}")
    
    if not os.path.exists(src_dir):
        print(f"Warning: Source directory {src_dir} not found. Skipping file copy.")
    else:

        # Move all files to unified directory
        print("Moving PDFs to unified directory...")
        files_processed = 0
        dest_dir = os.path.join(Config.PDF_DIR, 'unified')
        
        for filename in os.listdir(src_dir):
            if filename.endswith(".pdf"):
                shutil.copy2(os.path.join(src_dir, filename), os.path.join(dest_dir, filename))
                files_processed += 1
        
        print(f"Moved {files_processed} files.")
    
    print("Importing LangChain components...")
    from langchain_community.document_loaders import PyPDFLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_community.vectorstores import FAISS
    from langchain_huggingface import HuggingFaceEmbeddings
    
    # Embedding model
    print(f"Loading embedding model: {Config.FREE_EMBEDDING_MODEL}")
    try:
        embeddings = HuggingFaceEmbeddings(
            model_name=Config.FREE_EMBEDDING_MODEL,
            model_kwargs={'device': 'cpu'}
        )
    except Exception as e:
        print(f"HuggingFaceEmbeddings failed: {e}. Trying direct import...")
        from langchain_community.embeddings import HuggingFaceEmbeddings as HFEmbeddings
        embeddings = HFEmbeddings(
            model_name=Config.FREE_EMBEDDING_MODEL,
            model_kwargs={'device': 'cpu'}
        )
    
    # Process each category
    for category in ['unified']:
        print(f"Processing {category} PDFs...")
        
        pdf_folders = []
        if category == 'unified':
            pdf_folders = [os.path.join(Config.PDF_DIR, 'unified')]
        else:
            pdf_folders = [os.path.join(Config.PDF_DIR, category)]
            
        documents = []
        for pdf_folder in pdf_folders:
            if not os.path.exists(pdf_folder): continue
            for filename in os.listdir(pdf_folder):
                if filename.endswith(".pdf"):
                    file_path = os.path.join(pdf_folder, filename)
                    print(f"Loading {filename} from {os.path.basename(pdf_folder)}...")
                    try:
                        loader = PyPDFLoader(file_path)
                        documents.extend(loader.load())
                    except Exception as e:
                        print(f"Error loading {filename}: {e}")
        
        if not documents:
            print(f"No documents found for {category}")
            continue
            
        # Split text
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP
        )
        splits = text_splitter.split_documents(documents)
        
        # Create Vector Store
        print(f"Creating vector store for {category} ({len(splits)} chunks)...")
        vector_store = FAISS.from_documents(splits, embeddings)
        
        # Save Vector Store
        save_path = os.path.join(Config.VECTOR_DB_DIR, category)
        vector_store.save_local(save_path)
        print(f"Saved {category} vector store to {save_path}")

if __name__ == "__main__":
    process_pdfs()
