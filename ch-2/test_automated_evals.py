from run_evals import evaluate_generated_answer, evals, eval_answers

def run_RAG(user_question):
    return "IDKLOL"

def test_run_RAG():
    generated_answers = []
    for question in evals:
        answer = run_RAG(question)
        generated_answers.append(answer)

    for i in range(len(evals)):
        result = evaluate_generated_answer(eval_answers[i], generated_answers[i])
        assert "PASS" in result
