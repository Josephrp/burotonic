# ./src/memories/localloader.py

# add import statements
# Load data/documents

# why not reuse vector.py?
import chromadb
import os  #see chat
import chromadb.utils.embedding_functions as embedding_functions
from langchain.document_loaders import DirectoryLoader,TextLoader

from langchain_openai import OpenAIEmbeddings
# :-) ill explain you later 
UnstructuredReader = download_loader('UnstructuredReader')
dir_reader = SimpleDirectoryReader(r"/add_your_files_here/", file_extractor={
    ".pdf": UnstructuredReader(),
    ".html": UnstructuredReader(),
    ".eml": UnstructuredReader(),
    ".xlsx": UnstructuredReader()
}, recursive=True)

documents = dir_reader.load_data()

# Create vector store/embeddings
vector_store_directory = "./src/vector_store"
os.makedirs(vector_store_directory, exist_ok=True)
db = chromadb.PersistentClient(path=vector_store_directory) #create dir if dont exist ? okay 
chroma_client = chromadb.EphemeralClient()
chroma_collection = chroma_client.create_collection("collection_name")
embed_model = OpenAIEmbeddings(openai_api_key="...") # move this to open ai embeddings

# Extracting metadata and creating nodes
text_splitter = TokenTextSplitter(separator=" ", chunk_size=1024, chunk_overlap=128)
metadata_extractor = MetadataExtractor(extractors=[TitleExtractor(nodes=5), QuestionsAnsweredExtractor(questions=3)])
node_parser = SimpleNodeParser.from_defaults(text_splitter=text_splitter)

# Set up ChromaVectorStore and load in data
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
service_context = ServiceContext.from_defaults(embed_model=embed_model, node_parser=node_parser)
index = VectorStoreIndex.from_documents(documents, storage_context=storage_context, service_context=service_context)

# Custom context retrieval function
def query_vector_db(query_texts: List[str], n_results: int = 10, search_string: str = "", **kwargs) -> Dict[str, List[List[Any]]]:
    result_dict = {"ids": [], "documents": []}
    # Custom query logic goes here...
    return result_dict

# move below to agentics (?)
class LocalRetrieveUserProxyAgent(RetrieveUserProxyAgent):
    def query_vector_db(self, query_texts: List[str], n_results: int = 5, search_string: str = "", **kwargs) -> Dict[str, List[List[Any]]]:
        return query_vector_db(query_texts, n_results, search_string, **kwargs)

    def retrieve_docs(self, problem: str, n_results: int = 5, search_string: str = "", **kwargs):
        results = self.query_vector_db(query_texts=[problem], n_results=n_results, search_string=search_string, **kwargs)
        self._results = results
        print("doc_ids: ", results["ids"])