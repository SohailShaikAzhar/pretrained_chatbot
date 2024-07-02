import json
#difflib helps to find the differences between strings or any data type which is hashable(dict)
#get_close_matches helps to get the best matches which we give as input based on the percentage of matching of strings
from difflib import get_close_matches

#load the knowledge base from json file 
def load_knowledge_base(file_path: str)-> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

#opening 
def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

#finding the best match based on the input given 
def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

#Finding the answer to the question
def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]
    

def chat_bot():
    #assigning the knowledge_base as dict from json file
    knowledge_base: dict = load_knowledge_base('knowledge_base.json')

    #taking the input from the user
    while True:
        user_input: str = input('You: ')
        if user_input.lower() == 'quit':
            break

        #finding the matching string with the user input for the output
        best_match: str | None = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])
        if best_match:
            answer: str = get_answer_for_question(best_match, knowledge_base)
            print(f'Bot: {answer}')
        else:
            print('Bot: I don\'t know the answer. Can you teach me?')
            new_answer: str = input('Type the answer or "skip" to skip: ')

            if new_answer.lower() != 'skip':
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                save_knowledge_base('knowledge_base.json', knowledge_base)
                print('Bot: Thank you! I learned a new response!')

if __name__ == '__main__':
    chat_bot()
