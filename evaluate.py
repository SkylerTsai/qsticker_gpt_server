import langsmith
from langchain import chat_models, smith

from src.dependencies.settings import get_settings
from src.service.math_solver import MathSolver

# Define your runnable or chain below.
math_solver = MathSolver(model="gpt-4-1106-preview", temperature=0).agent

# Define the evaluators to apply
eval_config = smith.RunEvalConfig(
    evaluators=[
        "cot_qa",
        smith.RunEvalConfig.LabeledCriteria("helpfulness"),
        smith.RunEvalConfig.LabeledCriteria("conciseness")
    ],
    custom_evaluators=[],
    eval_llm=chat_models.ChatOpenAI(model="gpt-3.5-turbo", 
        temperature=0, 
        openai_api_key=get_settings().gpt_secret_key
    )
)

client = langsmith.Client()
chain_results = client.run_on_dataset(
    dataset_name="hanlin math grade 1",
    llm_or_chain_factory=math_solver,
    evaluation=eval_config,
    project_name="QSticker Math APP evaluator",
    concurrency_level=5,
    verbose=True,
)