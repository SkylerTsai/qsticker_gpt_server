import chainlit as cl
from src.service.math_solver import MathSolver
from src.service.translator import Translator
from src.service.question_generator import QuestuionGenerator

math_solver = MathSolver()
translator = Translator()
questuion_generator = QuestuionGenerator()

async def YesOrNo(msg):
    res = await cl.AskActionMessage(
        content=msg,
        actions=[
            cl.Action(name="YES", value="YES", label="✅ 是"),
            cl.Action(name="NO", value="NO", label="❌ 否"),
        ],
        raise_on_timeout=False,
    ).send()
    if res:
        return res.get("value")
    return None

@cl.on_chat_start
async def chatbot():
    print("hello", cl.user_session.get("id"))
    cl.user_session.set("agent", math_solver.agent)
    actions = [
        cl.Action(name="SAQ", value="SAQ", label="簡答題", description="只有數學題目本身"),
        cl.Action(name="MCQ", value="MCQ", label="選擇題", description="包含數學題目及四個選項"),
    ]
    await cl.Message(content="請直接輸入題目或選擇要回答的題目類型:", actions=actions).send()

@cl.on_chat_end
async def chatbot():
    print("goodbye", cl.user_session.get("id"))

@cl.on_message
async def on_message(message: cl.Message):
    await solve(message.content, math_solver.SAQ_prompt(message.content))

@cl.action_callback("SAQ")
async def SAQ():
    res = await cl.AskUserMessage(content="請輸入問題").send()
    if res:  
        await solve(res['output'], math_solver.SAQ_prompt(res['output']))

@cl.action_callback("MCQ")
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

    await solve(mcq['question'], math_solver.MCQ_prompt(mcq), "MCQ")

async def get_solution(input):
    agent = cl.user_session.get("agent")
    response = await agent.acall(
        {"input":input},
        callbacks=[cl.AsyncLangchainCallbackHandler()]\
    )

    solution = translator.translate(response["output"])
    await cl.Message(solution).send()

async def solve(question, input, type="SAQ"):
    solved = False
    solution = None
    while not solved:
        await get_solution(input)

        yn = await YesOrNo("以上解答內容正確嗎?")

        if yn == "YES":
            solved = True
        elif yn == "NO":
            await cl.Message("重新計算答案").send()
        else:
            await cl.Message("等候時間過長，請重新開始").send()
            break
    
    if solved:
        await generate_new_quesstion(question, solution)

async def generate_new_quesstion(question, solution):
    yn = await YesOrNo("是否以此題生成新問題?")
    if yn != "YES": 
        await cl.Message("對話結束").send()

    finished = False
    while not finished:
        question_prompt = questuion_generator.question_generation_prompt(question)
        new_question = questuion_generator.reply(question_prompt)
        await cl.Message(new_question).send()
        await get_solution(math_solver.SAQ_prompt(new_question))
        
        yn = await YesOrNo("是否要更重新生成題目")
        if yn == "YES":
            await cl.Message("重新生成題目").send()
        elif yn == "NO":
            finished = True
        else:
            await cl.Message("等候時間過長，請重新開始").send()
            break

    await cl.Message("對話結束").send()