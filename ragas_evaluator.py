from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from typing import Dict, List, Optional

# RAGAS imports
try:
    from ragas import SingleTurnSample, EvaluationDataset
    from ragas.metrics import BleuScore, NonLLMContextPrecisionWithReference, ResponseRelevancy, Faithfulness, RougeScore
    from ragas import evaluate
    RAGAS_AVAILABLE = True
except ImportError:
    RAGAS_AVAILABLE = False

def evaluate_response_quality(question: str, answer: str, contexts: List[str]) -> Dict[str, float]:
    """Evaluate response quality using RAGAS metrics"""
    if not RAGAS_AVAILABLE:
        return {"error": "RAGAS not available"}
    
    # TODO: Create evaluator LLM with model gpt-3.5-turbo
    evaluator_llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-3.5-turbo"))
    
    # TODO: Create evaluator_embeddings with model test-embedding-3-small
    evaluator_embeddings = LangchainEmbeddingsWrapper(OpenAIEmbeddings(model="text-embedding-3-small"))
    
    # TODO: Define an instance for each metric to evaluate
    metrics = [
        ResponseRelevancy(),
        Faithfulness(),
     ]

    """ metrics = [
        BleuScore(),
        NonLLMContextPrecisionWithReference(),
        ResponseRelevancy(),
        Faithfulness(),
        RougeScore(),
        AnswerRelevancy
     ]"""

    if "BlueScore" in metrics:
        metrics.append(BleuScore())
    if "RougeScore" in metrics:
        metrics.append(RougeScore())

    sample = SingleTurnSample(user_input=question, response=answer, retrieved_contexts=contexts)
    
    # TODO: Evaluate the response using the metrics    
    
    try:

        dataset = EvaluationDataset([sample])
        
        results = evaluate(dataset, metrics, evaluator_llm, evaluator_embeddings)
        
        # TODO: Return the evaluation results

        dataframe = results.to_pandas()

        return dataframe.iloc[0].to_dict()
            
    except Exception as e:
        return {"error": str(e)}

