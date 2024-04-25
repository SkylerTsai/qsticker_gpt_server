import langsmith
from langchain import chat_models, smith
from langchain_openai import ChatOpenAI
from src.service.math_solver import MathSolver
from src.dependencies.settings import get_settings


math_solver = MathSolver()

# Define the evaluators to apply
eval_config = smith.RunEvalConfig(
    evaluators=[
        "cot_qa"
    ],
    custom_evaluators=[],
    eval_llm=ChatOpenAI(model="gpt-4", temperature=0, openai_api_key=get_settings().gpt_secret_key)
)

client = langsmith.Client()
chain_results = client.run_on_dataset(
    dataset_name="Hanlin Elementary School Mathematics 1",
    llm_or_chain_factory=math_solver.agent,
    evaluation=eval_config,
    project_name="test-qsticker",
    concurrency_level=5,
    verbose=True,
)