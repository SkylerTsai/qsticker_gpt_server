import chainlit as cl
from langchain.prompts import PromptTemplate
from src.service.langchain_service import LangChainService

@cl.on_chat_start
async def chatbot():
    service = LangChainService()
    cl.user_session.set("agent", service.agent)

@cl.on_message
async def on_message(message: cl.Message):    
    res = await cl.AskActionMessage(
        content="要回答簡答題還是選擇題",
        actions=[
            cl.Action(name="SAQ", value="SAQ", label="簡答題"),
            cl.Action(name="MCQ", value="MCQ", label="選擇題"),
        ],
    ).send()

    if res and res.get("value") == "SAQ":
        await SAQ()

    elif res and res.get("value") == "MCQ":
        await MCQ()

async def MCQ():
    prompt_template = PromptTemplate.from_template(
        """
        The following is a math question and 4 options
        Quesrion: {question}
        A: {option_1}
        B: {option_2}
        C: {option_3}
        D: {option_4}
        Please solve the question and return the answer and solution in the the format and tralate to zh-TW
        Answer: the correct option A, B, C, or D
        Solution: the way to solve the question, clearly detail the steps involved and give the final answer. Provide the response in bullet points.
        """
    )
    mcq = {}
    res = await cl.AskUserMessage(content="請輸入問題").send()
    if res:
        mcq['question'] = res['output']
    res = await cl.AskUserMessage(content="請輸入選項1").send()
    if res:
        mcq['option_1'] = res['output']
    res = await cl.AskUserMessage(content="請輸入選項2").send()
    if res:
        mcq['option_2'] = res['output']
    res = await cl.AskUserMessage(content="請輸入選項3").send()
    if res:
        mcq['option_3'] = res['output']
    res = await cl.AskUserMessage(content="請輸入選項4").send()
    if res:
        mcq['option_4'] = res['output']

    await ask(prompt_template.format(
        question = mcq["question"], 
        option_1 = mcq["option_1"],
        option_2 = mcq["option_2"],
        option_3 = mcq["option_3"],
        option_4 = mcq["option_4"],
    ))
    
async def SAQ():
    prompt_template = PromptTemplate.from_template(
        """
        The following is a math question
        Quesrion: {question}
        Please solve the question and return the answer and solution in the format and tralate to zh-TW
        Answer: the brief answer
        Solution: the way to solve the question, clearly detail the steps involved and give the final answer. Provide the response in bullet points.
        """
    )

    res = await cl.AskUserMessage(content="請輸入問題").send()
    if res:  
        await ask(prompt_template.format(question = res['output']))

async def ask(msg):
    agent = cl.user_session.get("agent")

    response = await agent.acall(
        msg,
        callbacks=[cl.AsyncLangchainCallbackHandler()]\
    )

    await cl.Message(response["output"]).send()