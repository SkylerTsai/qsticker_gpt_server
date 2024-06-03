from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from src.dependencies.settings import get_settings

class QuestionEvaluator:
    def __init__(self, model="gpt-4-1106-preview", temperature=0., tools=[]) -> None:
        self.llm_init(model, temperature)
    
    def llm_init(self, model, temperature):
        self.llm = ChatOpenAI(
            model=model,
            temperature=temperature,
            api_key=get_settings().gpt_secret_key,
        )

    def QA_evaluation_prompt(self, question, solution):
        prompt_template = PromptTemplate.from_template("""
You are a teacher evaluate a question and solution.
You are given a question abd corresponding answer and solution. 
You are asked to evaluate the question and the solution's rationality as either CORRECT or INCORRECT.
For example, if the age of a person is not integer or less than zero, it is incorrect.
If the question or the answer is not rational, please write down the explanation.

Example Format:
QUESTION: question here
ANSWER AND SOLUTION: student's answer and solution here
EXPLANATION: 
RATIONALITY: 

Grade the student answers based ONLY on their factual accuracy. 
Ignore the correctness of the equations in the answer and solution. Begin!

QUESTION: {question}
ANSWER AND SOLUTION: {solution}
EXPLANATION:
"""
        )
        return prompt_template.format(question=question, solution=solution)


    def cot_evaluation_prompt(self, question, solution):
        prompt_template = PromptTemplate.from_template("""
You are a teacher grading a quiz.
You are given a question the student's answer and solution. 
You are asked to score the student's answer as either CORRECT or INCORRECT.
Write out in a step by step manner your reasoning to be sure that your conclusion is correct. 
Avoid simply stating the correct answer at the outset.

Example Format:
QUESTION: question here
STUDENT ANSWER AND SOLUTION: student's answer and solution here
EXPLANATION: step by step reasoning here
GRADE: CORRECT or INCORRECT here

Grade the student answers based ONLY on their factual accuracy. 
Ignore differences in punctuation and phrasing between the student answer and true answer. 
It is OK if the student answer contains more information than the true answer, as long as it does not contain any conflicting statements. Begin! 

QUESTION: {question}
STUDENT ANSWER AND SOLUTION: {solution}
EXPLANATION:
"""
        )
        return prompt_template.format(question=question, solution=solution)

    def reply(self, msg):
        return self.llm.invoke(msg).content

