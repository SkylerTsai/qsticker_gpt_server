import chainlit as cl
from src.service.math_solver import MathSolver
from src.service.translator import Translator

math_solver = MathSolver()
translator = Translator()

@cl.on_chat_start
async def chatbot():
    cl.user_session.set("agent", math_solver.agent)

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

    await ask(math_solver.MCQ_prompt(mcq))
    
async def SAQ():
    res = await cl.AskUserMessage(content="請輸入問題").send()
    if res:  
        await ask(math_solver.SAQ_prompt(res['output']))

async def ask(msg):
    agent = cl.user_session.get("agent")

    response = await agent.acall(
        {"input":msg},
        callbacks=[cl.AsyncLangchainCallbackHandler()]\
    )

    ret = translator.translate(response["output"])

    if ret:
        await cl.Message(ret).send()