import chromadb
from langchain.document_loaders import DirectoryLoader,TextLoader
#from src.plugins.websearch.search import WebScraper
from search import WebScraper
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceInstructEmbeddings,SentenceTransformerEmbeddings,HuggingFaceEmbeddings
from langchain.vectorstores import Chroma


# loader =DirectoryLoader('./website_data',glob='./*.txt',loader_cls=TextLoader)
# documents=loader.load()
# text_splitter=RecursiveCharacterTextSplitter(chunk_size=1008,chunk_overlap=200)
# texts=text_splitter.split_documents(documents)
# persist_directory="./src/vector_store"
# instructor_embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl",
#                                                       model_kwargs={"device": "cpu"})
# def querry():
#     embedding = instructor_embeddings
#     vectordb = Chroma.from_documents(documents=texts,
#                                     embedding=embedding,
#                                     persist_directory=persist_directory)
#     retriever = vectordb.as_retriever(search_kwargs={"k": 5})
#     vectordb.presist()



class vector:
    def __init__(self, query, num_results=10, output_folder="./website_data", vector_store_path="./src/vector_store", collection_name="web_collection"):
        self.query = query
        self.num_results = num_results
        self.output_folder = output_folder
        self.vector_store_path = vector_store_path
        self.collection_name = collection_name
        self.scraper = WebScraper(query, num_results, output_folder)
        self.db = chromadb.PersistentClient(path=r"./src/vector_store")
        self.chroma_collection = None
        self.vector_store = None
        self.documents = []
    def scrape_and_save(self):
        """Scrape web pages and save the content to files."""
        self.scraper.run()
    # def load_data(self):
    #     loader = DirectoryLoader('./website_data', glob='**/*.txt')
    #     documents = loader.load()

    #     text_splitter = RecursiveCharacterTextSplitter(chunk_size=1008, chunk_overlap=200)
    #     self.texts = []

    #     for document in documents:
    #         try:
    #             with open(document.file_path, 'rb') as file:
    #                 raw_content = file.read()
    #                 possible_encodings = ['utf-8', 'cp1252', 'latin-1']  # Add more encodings if needed
    #                 for encoding in possible_encodings:
    #                     try:
    #                         text = raw_content.decode(encoding)
    #                         self.texts.extend(text_splitter.split(text))
    #                         break  # Break if decoding is successful
    #                     except UnicodeDecodeError:
    #                         continue  # Try the next encoding
    #         except Exception as e:
    #             print(f"Error loading file {document.file_path}: {e}")

    #     if not self.texts:
    #         print("No valid text found in the loaded documents.")


    def load_data(self):
         loader = DirectoryLoader('./website_data', glob='**/*.txt')
         documents=loader.load()
         text_splitter=RecursiveCharacterTextSplitter(chunk_size=1008,chunk_overlap=200)
         self.texts=text_splitter.split_documents(documents)
    def setup_vector_store(self):
        model_name = "intfloat/e5-large-v2"
        #instructor_embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl",model_kwargs={"device": "cpu"})
        

        persist_directory="./src/plugins/websearch/db/"
        embedding=HuggingFaceEmbeddings(model_name=model_name)
        #embedding = instructor_embeddings
        vectordb = Chroma.from_documents(documents=self.texts,
                                        embedding=embedding,
                                        persist_directory=persist_directory)
        vectordb.persist()
        retriever = vectordb.as_retriever(search_kwargs={"k": 5})
        
    def setup(self):
        """Run the complete process: scrape, load, setup vector store, and ready for querying."""
        print("Starting web scraping...")
        self.scrape_and_save()
        print("Loading data...")
        self.load_data()
        print("Setting up vector store and indexing documents...")
        self.setup_vector_store()
        print("Setup complete. The agent is now ready to query.")      
vec=vector("what is LLM")
vec.setup()





