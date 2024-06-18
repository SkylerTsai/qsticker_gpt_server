import chainlit as cl
from chainlit.input_widget import Select, Slider, Switch
from chainlit.types import ThreadDict
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.schema.runnable.config import RunnableConfig
from typing import Optional
from src.service.math_solver import MathSolver
from src.service.translator import Translator
from src.service.question_generator import QuestionGenerator
from src.service.question_evaluator import QuestionEvaluator
from src.service.QSticker_service import QStickerService
from src.controller.QSticker.schema.user_info import UserInfoRequestBody


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
    #cl.user_session.set("memory", ChatMessageHistory(session_id=cl.user_session.get("id")))

    settings = await cl.ChatSettings(
        [
            Select(
                id="Model",
                label="OpenAI Chat Model",
                values=["gpt-3.5-turbo-0125", "gpt-4-1106-preview", "gpt-4o"],
                initial_index=0,
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
            Switch(
                id="Generate-enabled",
                label="Generate New Question",
                initial=True,
            ),
            Slider(
                id="Maximum-generation",
                label="Maximum Question Generate Number",
                initial=2,
                min=1,
                max=10,
                step=1,
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
    cl.user_session.set("question_generator", QuestionGenerator(
        model=settings["Model"], 
        temperature=settings["Temperature"],
    ))
    cl.user_session.set("question_evaluator", QuestionEvaluator(
        model=settings["Model"], 
        temperature=settings["Temperature"],
    ))
    cl.user_session.set("human_intervention", settings["Human-intervention"])
    cl.user_session.set("generate_enabled", settings["Generate-enabled"])
    cl.user_session.set("maximum_generation", settings["Maximum-generation"])


@cl.on_chat_end
async def end() -> None:
    print("goodbye", cl.user_session.get("id"))


# @cl.on_chat_resume
# async def on_chat_resume(thread: ThreadDict):
#     print("The user resumed a previous chat session!")
#     print(cl.user_session)


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
    await get_solution(message.content)


@cl.action_callback("SAQ")
async def SAQ() -> None:
    res = await askMessage("請輸入問題")
    if res:  
        await get_solution(res)


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

    await get_solution(MathSolver.MCQ_to_SAQ(mcq), "MCQ")


@cl.step
async def translating(question, solution) -> dict:
    translator = cl.user_session.get("translator")
    if solution:
        prompt = translator.question_solution_prompt(question, solution)
    else:
        prompt = translator.question_prompt(question)

    res = await translator.allm_translate(prompt)
    return res


@cl.step
async def solving(question) -> dict:
    agent = cl.user_session.get("agent")
    question_prompt = MathSolver.SAQ_prompt(question)
    response = await agent.ainvoke(
        {"input":question_prompt},
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
        #callbacks=[cl.AsyncLangchainCallbackHandler()]\
    )
    # await reply(response['output'])
    
    solution = await translating(question, response['output'])
    res = {
        'input': question,
        'output': solution,
        #'intermediate_steps': response['intermediate_steps'],
    }
    return res


@cl.step
async def generating(question, solution) -> dict:
    generator = cl.user_session.get("question_generator")
    question_prompt = generator.question_generation_prompt(question, solution)
    new_question = await generator.areply(question_prompt)
    new_question = await translating(new_question, None)

    return {'output': new_question}


@cl.step
async def evaluating(question, solution) -> dict:
    evaluator = cl.user_session.get("question_evaluator")
    res = {}
    res['QA'] = await evaluator.areply(evaluator.QA_evaluation_prompt(question, solution))
    res['COT'] = await evaluator.areply(evaluator.cot_evaluation_prompt(question, solution))
    
    return res

async def get_solution(question, type="SAQ") -> None:
    solved = False
    while not solved:
        response = await solving(question)
        await cl.Message(content=response["output"]).send()

        if cl.user_session.get("human_intervention"):
            yn = await YesOrNo("是否重新生成解答?")
            if yn == "YES":
                await reply("重新計算答案...")
            elif yn == "NO":
                solved = True
            else:
                await reply("等候時間過長，請重新開始")
                break
        else:
            res = await evaluating(response['input'], response['output'])
            if res and res['QA'] and res['COT']:
                if 'RATIONALITY: CORRECT' in res['QA'] and 'GRADE: CORRECT' in res['COT']: 
                    solved = True
    
    if solved and cl.user_session.get("generate_enabled"):
        await generate_new_quesstion(response)
    else:
        await reply("解題完成，對話結束")


async def generate_solve_evaluate(question, solution) -> dict:
    generate_time = 0
    new_question = None
    new_solution = None
    while generate_time < cl.user_session.get("maximum_generation"):
        new_question, new_solution, eval = None, None, None
        res = await generating(question, solution)
        if res: new_question = res['output']
        res = await solving(new_question)
        if res: new_solution = res['output']
        res = await evaluating(new_question, new_solution)
        if res and res['QA'] and res['COT']:
            qa = 'CORRECT' in res['QA'] and 'INCORRECT' not in res['QA']
            cot = 'CORRECT' in res['COT'] and 'INCORRECT' not in res['COT']
            if qa and cot: break
        generate_time += 1
        
    if generate_time == cl.user_session.get("maximum_generation"): return None
    return {
        'question': new_question if generate_time < cl.user_session.get("maximum_generation") else None,
        'solution': new_solution if generate_time < cl.user_session.get("maximum_generation") else None,
    }


async def generate_new_quesstion(response) -> None:
    question, solution = response['input'], response['output']

    finished = False
    while not finished:
        await reply("題目生成中...")

        res = await generate_solve_evaluate(question, solution)
        if res:
            await cl.Message(content=res['question']).send()
            await cl.Message(content=res['solution']).send()
        else:
            await reply("題目生成失敗")
            break
        
        yn = await YesOrNo("是否重新生成題目")
        if yn == "NO":
            finished = True
        else:
            await reply("等候時間過長，請重新開始")
            break

    await reply("對話結束")
