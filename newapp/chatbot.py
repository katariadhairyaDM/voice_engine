
resp = {
    "hi" : "Hello",
    "hello" : "Hello",
    "morning" : "Hi, Good Morning",
    "afternoon" : "Hi, Good Afternoon",
    "evening" : "Hi, Good Evening",
    "hello" : "Hello",
    'how are you' : "I'm doing good \nHow about You ?",
    "i am fine" : "Great to hear that, How can I help you?",
    "i am good" : "Great to hear that, How can I help you?",
    "help me" : "I can show you the Data according to you'r query"
}

def ChatBot(query):
    for que, ans in resp.items():
        if que in query:
            return ans
    return ''

# print(ChatBot('good morning'))