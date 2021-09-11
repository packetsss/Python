# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

class Question:
    def __init__(self, prompt, answer):
        self.prompt = prompt
        self.answer = answer


question_prompt = [
    "What color is Apple?\n(a)red\n(b)green\n(c)yellow\n\n",
    "What color is Orange?\n(a)red\n(b)orange\n(c)green\n\n",
    "What color is Lemon?\n(a)yellow\n(b)orange\n(c)green\n\n",
]

questions = [
    Question(question_prompt[0], "a"),
    Question(question_prompt[1], "b"),
    Question(question_prompt[2], "a"),
]


def test(question):
    score = 0
    for question in questions:
        answer = input("\n".join(question_prompt))
        if answer == question.answer:
            score += 1
    print("You got " + str(score) + "/" + str(len(questions)) + " correct.")


test(question_prompt)
