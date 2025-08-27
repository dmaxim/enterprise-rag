import openai
import os

evals = [
    "What is Underwhelming Spatula?",
    "Who wrote 'Dubious Parenting Tips'?",
    "How long is Almost-Perfect Investment Guid?"
]

eval_answers = [
    "Underwhelming Spatula is a kitchen tool that redefines expectations by fusing whimsy with functionality.",
    "The book 'Dubious Parenting Tips' was written by Lisa Melton",
    "The 'Almost-Perfect Investment Guide' is 120 pages long."
]

def send_to_openai(message):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    completion = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": message}],
    )
    print("response")
    return completion.choices[0].message.content.strip() # type: ignore

def evaluate_generated_answer(
        expected_answer,
        generated_answer): 
    prompt = f"""Please evaluate the generated answer.
    If the generated answer provides the same information as the expected answer,
    then return PASS. Otherwise, return FAIL.
    Expected Answer: {expected_answer}
    Generated Answer: {generated_answer}
    """
    return send_to_openai(prompt)