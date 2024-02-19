import autogen
from autogen import AssistantAgent
from autogen.agentchat.contrib.retrieve_user_proxy_agent import RetrieveUserProxyAgent
import chromadb

# # move below to agentics (?)
# class MyRetrieveUserProxyAgent(RetrieveUserProxyAgent):
#     def query_vector_db(self, query_texts: List[str], n_results: int = 10, search_string: str = "", **kwargs) -> Dict[str, List[List[Any]]]:
#         return query_vector_db(query_texts, n_results, search_string, **kwargs)

#     def retrieve_docs(self, problem: str, n_results: int = 20, search_string: str = "", **kwargs):
#         results = self.query_vector_db(query_texts=[problem], n_results=n_results, search_string=search_string, **kwargs)
#         self._results = results
#         print("doc_ids: ", results["ids"])