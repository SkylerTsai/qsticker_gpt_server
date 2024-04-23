import chainlit as cl
from chainlit.input_widget import Select, Slider
from src.service.math_solver import MathSolver
from src.service.translator import Translator
from src.service.question_generator import QuestuionGenerator


math_solver = MathSolver()
translator = Translator()
questuion_generator = QuestuionGenerator()


async def YesOrNo(msg):
    content = translator.translate(msg)
    res = await cl.AskActionMessage(
        content=content,
        actions=[
            cl.Action(name="YES", value="YES", label="✅ Yes"),
            cl.Action(name="NO", value="NO", label="❌ No"),
        ],
        raise_on_timeout=False,
    ).send()
    if res:
        return res.get("value")
    return None


async def reply(msg, actions=None):
    content = translator.translate(msg)
    await cl.Message(content=content, actions=actions).send()


async def askMessage(msg):
    content = translator.translate(msg)
    res = await cl.AskUserMessage(content=content).send()
    if res:  
        return res['output']
    return None


@cl.on_chat_start
async def chatbot():
    settings = await cl.ChatSettings(
        [
            Select(
                id="Model",
                label="OpenAI Chat Model",
                values=["gpt-3.5-turbo-0125", "gpt-4-1106-preview"],
                initial_index=1,
            ),
            Slider(
                id="Temperature",
                label="Temperature for Question Generation",
                initial=0.5,
                min=0,
                max=1,
                step=0.05,
            ),
            Select(
                id="Language",
                label="Respond Language",
                values=["zh-TW", "en"],
                initial_index=0,
            ),
        ]
    ).send()

    print("hello", cl.user_session.get("id"))
    cl.user_session.set("agent", math_solver.agent)
    actions = [
        cl.Action(name="SAQ", value="SAQ", label="Short Answer Question", description="Only question"),
        cl.Action(name="MCQ", value="MCQ", label="Multiple Choice Question", description="Question and 4 options"),
    ]
    await reply("請直接輸入題目或選擇要回答的題目類型:", actions)


@cl.on_settings_update
async def setup(settings):
    print("on_settings_update", settings)
    global math_solver
    math_solver.llm_init(model=settings["Model"])
    global translator
    translator.lang_init(lang=settings["Language"])
    global questuion_generator
    questuion_generator.llm_init(model=settings["Model"], temperature=settings["Temperature"])


@cl.on_chat_end
async def chatbot():
    print("goodbye", cl.user_session.get("id"))


@cl.on_message
async def on_message(message: cl.Message):
    await solve(math_solver.SAQ_prompt(message.content))


@cl.action_callback("SAQ")
async def SAQ():
    res = await askMessage("請輸入問題")
    if res:  
        await solve(math_solver.SAQ_prompt(res))


@cl.action_callback("MCQ")
async def MCQ():
    mcq = {}
    res = await askMessage("請輸入問題")
    if res:
        mcq['question'] = res
    res = await askMessage("請輸入選項1")
    if res:
        mcq['option_1'] = res
    res = await askMessage("請輸入選項2")
    if res:
        mcq['option_2'] = res
    res = await askMessage("請輸入選項3")
    if res:
        mcq['option_3'] = res
    res = await askMessage("請輸入選項4")
    if res:
        mcq['option_4'] = res

    await solve(math_solver.MCQ_prompt(mcq), "MCQ")


async def get_solution(input):
    agent = cl.user_session.get("agent")
    response = await agent.acall(
        {"input":input},
        callbacks=[cl.AsyncLangchainCallbackHandler()]\
    )
    await reply(response["output"])

    return response

async def solve(input, type="SAQ"):
    solved = False
    while not solved:
        response = await get_solution(input)

        yn = await YesOrNo("以上解答內容正確嗎?")

        if yn == "YES":
            solved = True
        elif yn == "NO":
            await reply("重新計算答案")
        else:
            await reply("等候時間過長，請重新開始")
            break
    
    if solved:
        yn = await YesOrNo("是否以此題生成新問題?")
        if yn == "YES": 
            await generate_new_quesstion(response)
        else:
            await reply("對話結束")


async def generate_new_quesstion(response):    
    question, solution, steps = response['input'], response['output'], response['intermediate_steps']

    finished = False
    while not finished:
        await reply("題目生成中...")
        question_prompt = questuion_generator.question_generation_prompt(question, solution)
        new_question = questuion_generator.reply(question_prompt)
        await reply(new_question)
        await get_solution(math_solver.SAQ_prompt(new_question))
        
        yn = await reply("是否要更重新生成題目")
        if yn == "NO":
            finished = True
        else:
            await reply("等候時間過長，請重新開始")
            break

    await reply("對話結束")

'''
題目->題目 X
題目+過程->題目
題目->過程->倒推過程->題目 X
'''