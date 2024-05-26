import chainlit as cl
from chainlit.input_widget import Select, Slider, Switch
from chainlit.types import ThreadDict
from langchain.memory import ChatMessageHistory
from typing import Optional
from src.service.math_solver import MathSolver
from src.service.translator import Translator
from src.service.question_generator import QuestuionGenerator
from src.service.QSticker_service import QStickerService
from src.controller.QSticker.schema.user_info import UserInfoRequestBody, UserInfoResponseBody


async def YesOrNo(msg) -> Optional[str]:
    content = cl.user_session.get("translator").translate(msg)
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


async def reply(msg, actions=None) -> None:
    content = cl.user_session.get("translator").translate(msg)
    await cl.Message(content=content, actions=actions).send()


async def askMessage(msg) -> Optional[str]:
    content = cl.user_session.get("translator").translate(msg)
    res = await cl.AskUserMessage(content=content).send()
    if res:  
        return res['output']
    return None


@cl.on_chat_start
async def start() -> None:
    cl.user_session.set("memory", ChatMessageHistory(session_id=cl.user_session.get("id")))

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
                max=2,
                step=0.1,
            ),
            Select(
                id="Language",
                label="Respond Language",
                values=["zh-TW", "en"],
                initial_index=0,
            ),
            Switch(
                id="Human-intervention",
                label="Enable human intervention",
                initial=True,
            ),
        ]
    ).send()

    await setup(settings)

    print("hello", cl.user_session.get("id"))
    actions = [
        cl.Action(name="SAQ", value="SAQ", label="Short Answer Question", description="Only question"),
        cl.Action(name="MCQ", value="MCQ", label="Multiple Choice Question", description="Question and 4 options"),
    ]
    await reply("請直接輸入題目或選擇要回答的題目類型:", actions)


@cl.on_settings_update
async def setup(settings: cl.ChatSettings) -> None:
    #print("on_settings_update", settings)
    cl.user_session.set("math_solver", MathSolver(
        model=settings["Model"], 
        temperature=settings["Temperature"],
    ))
    cl.user_session.set("agent", cl.user_session.get("math_solver").agent)
    cl.user_session.set("translator", Translator(
        model=settings["Model"], 
        temperature=settings["Temperature"], 
        lang=settings["Language"],
    ))
    cl.user_session.set("questuion_generator", QuestuionGenerator(
        model=settings["Model"], 
        temperature=settings["Temperature"],
    ))


@cl.on_chat_end
async def end() -> None:
    print("goodbye", cl.user_session.get("id"))


@cl.password_auth_callback
def auth_callback(account: str, password: str) -> Optional[cl.User]:
    if (account, password) == ("test", "test"):
        return cl.User(identifier=account)
    try:
        res = QStickerService().login(UserInfoRequestBody(account=account, password=password))
        return cl.User(identifier=res.username, token=res.token)
    except Exception:
        print(account + ' login failed!')
    return None


@cl.on_message
async def on_message(message: cl.Message) -> None:
    await solve(MathSolver.SAQ_prompt(message.content))


@cl.action_callback("SAQ")
async def SAQ() -> None:
    res = await askMessage("請輸入問題")
    if res:  
        await solve(MathSolver.SAQ_prompt(res))


@cl.action_callback("MCQ")
async def MCQ() -> None:
    mcq = {}
    res = await askMessage("請輸入問題")
    if res: mcq['question'] = res
    res = await askMessage("請輸入選項1")
    if res: mcq['option_1'] = res
    res = await askMessage("請輸入選項2")
    if res: mcq['option_2'] = res
    res = await askMessage("請輸入選項3")
    if res: mcq['option_3'] = res
    res = await askMessage("請輸入選項4")
    if res: mcq['option_4'] = res

    await solve(MathSolver.MCQ_prompt(mcq), "MCQ")


async def get_solution(input) -> dict:
    agent = cl.user_session.get("agent")
    response = await agent.acall(
        {"input":input},
        callbacks=[cl.AsyncLangchainCallbackHandler()]\
    )
    # await reply(response["output"])
    prompt = cl.user_session.get("translator").question_solution_prompt(input, response["output"])
    await cl.Message(content=cl.user_session.get("translator").llm_translate(prompt)).send()

    return response


async def solve(input, type="SAQ") -> None:
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


async def generate_new_quesstion(response) -> None:
    question, solution, steps = response['input'], response['output'], response['intermediate_steps']

    finished = False
    while not finished:
        await reply("題目生成中...")
        question_prompt = cl.user_session.get("questuion_generator").question_generation_prompt(question, solution)
        new_question = cl.user_session.get("questuion_generator").reply(question_prompt)
        await reply(new_question)
        await get_solution(MathSolver.SAQ_prompt(new_question))
        
        yn = await YesOrNo("是否要更重新生成題目")
        if yn == "NO":
            finished = True
        else:
            await reply("等候時間過長，請重新開始")
            break

    await reply("對話結束")
