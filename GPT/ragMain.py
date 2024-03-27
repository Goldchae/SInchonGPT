from langchain.chat_models import ChatOpenAI
import secret
from langchain.storage import LocalFileStore 
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import UnstructuredFileLoader
from langchain.embeddings import OpenAIEmbeddings, CacheBackedEmbeddings
from langchain.vectorstores import Chroma 
from langchain.chains import RetrievalQA 

# 모델 가져오기
llm = ChatOpenAI(temperature = 0.1,
                 openai_api_key = secret.openai_api_key
                 ) 

# 저장소 만들기 
cache_dir = LocalFileStore("./.cache/")

# 문서 로드 
loader = UnstructuredFileLoader("./files/practice0.pdf")

# splitter : 문자열 쪼개기
splitter = CharacterTextSplitter.from_tiktoken_encoder(
    separator="\n",
    chunk_size=600,
    chunk_overlap=100,
)

# 로드된 문서 : splitter로 문자 쪼개기
docs = loader.load_and_split(text_splitter = splitter)

# 임베딩 
embeddings = OpenAIEmbeddings(openai_api_key = secret.openai_api_key)
cached_embeddings = CacheBackedEmbeddings.from_bytes_store(embeddings, cache_dir)

# Chroma  
vectorstore = Chroma.from_documents(docs, cached_embeddings)

# 체인 만들기 
chain = RetrievalQA.from_chain_type(
    llm=llm, 
    retriever = vectorstore.as_retriever(), 
)

# 질문!
def invoke_chain(question):
    answer = chain.run(question) 
  
    return answer