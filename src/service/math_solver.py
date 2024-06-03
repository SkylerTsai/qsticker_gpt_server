from langchain.chains import LLMMathChain, LLMChain
from langchain.prompts import PromptTemplate
from langchain.agents import Tool, AgentExecutor, create_tool_calling_agent
from langchain_openai import ChatOpenAI
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.prompts import ChatPromptTemplate

from src.dependencies.settings import get_settings
from src.controller.langchain.schema.question_solution import QuestionSolution
from src.service.MyLLMSymbolicMathChain.base import LLMSymbolicMathChain

class MathSolver:
    def __init__(self, model="gpt-4-1106-preview", temperature=0) -> None:
        # llm
        self.llm_init(model, temperature)

        self.wiki_init()

        self.caculator_init()

        self.reasoning_init()
        
        self.sym_init()

        self.tools = [self.wiki_tool, self.math_tool, self.sym_tool, self.reasoning_tool]

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful assistant. Make sure to use the tools for information.",
                ),
                ("placeholder", "{chat_history}"),
                ("human", "{input}"),
                ("placeholder", "{agent_scratchpad}"),
            ]
        )
        
        self.tool_agent = create_tool_calling_agent(self.llm, self.tools, prompt)

        self.agent = AgentExecutor(
            agent = self.tool_agent,
            tools = self.tools,
            early_stopping_method='generate', # better be 'generate' but bug exist
            verbose=False,
            max_execution_time=60,
            max_iterations=10,
            handle_parsing_errors=True,
            return_intermediate_steps=True
        )


    def llm_init(self, model, temperature):
        self.llm = ChatOpenAI(
            model=model,
            temperature=temperature,
            api_key=get_settings().gpt_secret_key,
        )

    def wiki_init(self):
        self.wiki = WikipediaAPIWrapper()
        self.wiki_tool = Tool(
            name="Wikipedia",
            func=self.wiki.run,
            description="""
A useful tool for searching the Internet to find information on world events, issues, dates, years, etc. 
Worth using for general topics. 
Use precise questions.
""",
            handle_tool_error="Wikipedia execution failed, try to use other tool or change the input",
        )

    def caculator_init(self):
        self.math = LLMMathChain.from_llm(llm=self.llm)
        self.math_tool = Tool.from_function(
            name="Calculator",
            func=self.math.run,
            description="""
Useful for when you need to answer a single math expression. 
This tool is only for math questions and nothing else. 
Only input ONE math expression.
""",
            handle_tool_error="Calculator execution failed, try to use other tool or change the input",
        )
    
    def sym_init(self):
        self.sym = LLMSymbolicMathChain.from_llm(llm=self.llm)
        self.sym_tool = Tool.from_function(
            name="SymbolicMathSolver",
            func=self.sym.run,
            description="""
Useful for when you need to answer questions about symbolic math. 
This tool is only for symbolic math questions and nothing else. 
Only input math equations seperated by ','
""",
            handle_tool_error="SymbolicMathSolver execution failed, try to use other tool or change the input",
        )

    def reasoning_init(self):
        word_problem_template = """
You are a reasoning agent tasked with solving the user's logic-based questions. 
Logically arrive at the solution, and be factual. 
In your answers, clearly detail the steps involved and give the final answer. 
If it include math equations, stop at the step and return.
Provide the response in bullet points. 
Question: {question}
"""

        math_assistant_prompt = PromptTemplate(
            input_variables=["question"],
            template=word_problem_template,
        )

        self.reasoning = LLMChain(
            llm=self.llm,
            prompt=math_assistant_prompt,
        )

        self.reasoning_tool = Tool.from_function(
            name="ReasoningTool",
            func=self.reasoning.run,
            description="Useful for when you need to answer logic-based/reasoning questions.",
            handle_tool_error="ReasoningTool execution failed, try to use other tool or change the input",
        )

    def SAQ_prompt(saq):
        prompt_template = PromptTemplate.from_template("""
The following is a math question
Question: {question}
Please solve the question and return the answer and solution

Example Format: 
ANSWER: the answer ONLY
SOLUTION: the way to solve the question, briefly display the steps involved and give the final answer. 

Provide the response in bullet points. Enclose equations with two dollar signs ($). Begin!
"""
        )
        return prompt_template.format(question = saq)
    
    def MCQ_to_SAQ(mcq):
        return "{question} A: {option_1} B: {option_2} C: {option_3} D: {option_4}".format(
            question = mcq["question"], 
            option_1 = mcq["option_1"],
            option_2 = mcq["option_2"],
            option_3 = mcq["option_3"],
            option_4 = mcq["option_4"],
        )

    def question_reply(self, msg):
        return QuestionSolution(
            solution=self.agent.invoke({"input": msg})["output"],
        )
