from langchain.chains import LLMMathChain, LLMChain
from langchain.prompts import PromptTemplate
from langchain.agents.agent_types import AgentType
from langchain.agents import Tool, initialize_agent
from langchain_openai import ChatOpenAI
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.document_transformers import DoctranTextTranslator
from langchain_experimental.llm_symbolic_math.base import LLMSymbolicMathChain

from src.config.config import Settings
from src.dependencies.settings import get_settings
from src.controller.langchain.schema.question_solution import QuestionSolution


class LangChainService:
    def __init__(self) -> None:
        # llm
        self.llm = ChatOpenAI(
            model="gpt-4-1106-preview",
            temperature=0,
            api_key=get_settings().gpt_secret_key,
        )

        self.wiki_init()

        self.caculator_init()

        self.reasoning_init()
        
        self.sym_init()

        self.agent = initialize_agent(
            tools=[self.wiki_tool, self.math_tool, self.sym_tool, self.reasoning_tool],
            llm=self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            handle_parsing_errors=True,
            return_intermediate_steps=True
        )

    def wiki_init(self):
        self.wiki = WikipediaAPIWrapper()
        self.wiki_tool = Tool(
            name="Wikipedia",
            func=self.wiki.run,
            description="A useful tool for searching the Internet to find information on world events, issues, dates, years, etc. Worth using for general topics. Use precise questions.",
        )

    def caculator_init(self):
        self.math = LLMMathChain.from_llm(llm=self.llm)
        self.math_tool = Tool.from_function(
            name="Calculator",
            func=self.math.run,
            description="Useful for when you need to answer questions about math. This tool is only for math questions and nothing else. Only input math expressions.",
        )
    
    def sym_init(self):
        self.sym = LLMSymbolicMathChain.from_llm(llm=self.llm)
        self.sym_tool = Tool.from_function(
            name="Symbolic Math Solver",
            func=self.sym.run,
            description="Useful for when you need to answer questions about symbolic math. This tool is only for symbolic math questions and nothing else. Only input math equations or sympy code.",
        )

    def reasoning_init(self):
        word_problem_template = """You are a reasoning agent tasked with solving 
        the user's logic-based questions. Logically arrive at the solution, and be 
        factual. In your answers, clearly detail the steps involved and give the 
        final answer. Provide the response in bullet points. 
        Question  {question} Answer"""

        math_assistant_prompt = PromptTemplate(
            input_variables=["question"],
            template=word_problem_template,
        )

        self.reasoning = LLMChain(
            llm=self.llm,
            prompt=math_assistant_prompt,
        )

        self.reasoning_tool = Tool.from_function(
            name="Reasoning Tool",
            func=self.reasoning.run,
            description="Useful for when you need to answer logic-based/reasoning questions.",
        )

    def question_reply(self, msg):
        return QuestionSolution(
            solution=self.agent.invoke({"input": msg})["output"],
        )

    def MCQ_reply(self):
        return
