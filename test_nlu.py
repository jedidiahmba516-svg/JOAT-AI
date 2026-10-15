from engines.nlu_engine import analyze


questions = [
    "Who created Python?",
    "When was Microsoft founded?",
    "Where is Microsoft headquartered?",
    "What is Python?"
]


for question in questions:

    print("\n==============================")
    print("QUESTION:", question)

    result = analyze(question)

    print("RESULT:")
    print(result)