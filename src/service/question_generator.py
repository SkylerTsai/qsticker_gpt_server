from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from src.dependencies.settings import get_settings

class QuestuionGenerator:
    def __init__(self, model="gpt-4-1106-preview", temperature=0.8, tools=[]) -> None:
        self.llm_init(model, temperature)
    
    def llm_init(self, model, temperature):
        self.llm = ChatOpenAI(
            model=model,
            temperature=temperature,
            api_key=get_settings().gpt_secret_key,
        )

    def question_generation_prompt(self, question, solution):
        prompt_template = PromptTemplate.from_template(
            """
            The following is a math question and the solution
            Question: {question}
            Solution: {solution}
            Please construct a new similar question which has the same structure but with different objects and numbers
            Return in the following format
            New question:
            New solution:
            """
        )
        return prompt_template.format(question=question, solution=solution)
        
    def option_generation_prompt(self, question, answer):
        prompt_template = PromptTemplate.from_template(
            """
            The following is a math question and the correct answer
            Quesrion: {question}
            Answer: {answer}
            Please solve the question and return the answer and solution in the the following format
            Answer: the correct option A, B, C, or D
            Method: the way to solve the question, clearly detail the steps involved and give the final answer briefly. Provide the response in bullet points.
            """
        )
        return prompt_template.format(question=question, answer=answer)

    def reply(self, msg):
        return self.llm.invoke(msg).content
