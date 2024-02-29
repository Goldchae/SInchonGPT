from langchain.memory import ConversationSummaryBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.schema.runnable import RunnablePassthrough
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
import secret

llm = ChatOpenAI(temperature=0.1,openai_api_key=secret.openai_api_key) # 유의!!!!!

memory = ConversationSummaryBufferMemory(
    llm=llm,
    max_token_limit=1000,
    return_messages=True,
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "당신은 신촌 지역 대학교 알고리즘 연합 학회의 상담사입니다. 모든 대답은 한국어로 대답해 주세요."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ]
)


def load_memory(_):  # 메모리 변수들을 가져오는 함수
    return memory.load_memory_variables({})["history"]  # 메모리를 로드


chain = RunnablePassthrough.assign(
    history=load_memory) | prompt | llm  # 체인 만들기


def invoke_chain(author,question):
    result = chain.invoke({"question": question})  # invoke
    memory.save_context(  # 사람과 AI의 메세지를 메모리에 저장
        {"input": author +"은 '" + question  + "'이라고 네게 상담했어."},
        {"output": result.content},
    )
    print(result.content)
    print(memory.load_memory_variables({}))
    return result.content