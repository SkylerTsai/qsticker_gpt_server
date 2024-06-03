from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from src.dependencies.settings import get_settings

class QuestionGenerator:
    def __init__(self, model="gpt-4-1106-preview", temperature=0.8, tools=[]) -> None:
        self.llm_init(model, temperature)
    
    def llm_init(self, model, temperature):
        self.llm = ChatOpenAI(
            model=model,
            temperature=temperature,
            api_key=get_settings().gpt_secret_key,
        )

    def question_generation_prompt(self, question, solution):
        prompt_template = PromptTemplate.from_template("""
The following is a math question and the solution
Question: {question}
Solution: {solution}
Please construct a new similar question which has the same structure but with different objects and numbers.

Example Format:
New question: the new question here

Reply the new question only, don't reply the new solution. 
Enclose equations with two dollar signs ($). Begin!
New question:
"""
        )
        return prompt_template.format(question=question, solution=solution)

    def reply(self, msg):
        return self.llm.invoke(msg).content

    async def areply(self, msg):
        res = await self.llm.ainvoke(msg)
        return res.content