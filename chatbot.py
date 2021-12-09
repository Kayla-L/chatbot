from random import choice
import string

"""
Instructions:

0. Run the chatbot (there will be errors because there's missing code)
1. Fill in code for TODOs 1-5
2. Run the chatbot & get rid of all the errors, when you type "hi" into the
   prompt, the chatbot should respond, "Hello!"
3. Add 2 more intents (TODO 6)
4. Run the chatbot & get rid of all errors, get it to notice all 3 intents
5. Randomize response (TODO 7) and add responses to a greeting (TODO 8)
   HINT: use the library:
     import random
6. Run the chatbot & get rid of all errors, run multiple times to see it
   greet the user multiple ways
7. Modify the matching function (TODOs 9, 10, and optionally 11) to make the
   chatbot more likely to understand the user, even if they type things slightly
   differently than the pattern
8. Run the chatbot & get rid of all errors, see if it catches different versions
   of the user's utterances
9. Add an introduction (TODOs 12 & 13)
10. Run the chatbot & get rid of all errors
11. Modify the code so that the conversation ends when the user has the "goodbye" intent
12. Run the chatbot & get rid of all errors
13. Add riddles to the chatbot. (TODOs 14 & 15) Make a dictionary of all the riddles and answers
14. Run the chatbot & get rid of all errors 
15. (optional). Any other changes you want to make! 
"""

"""
Here's where we can store any variables the computer learns from the user.
"""
conversation_state = {
  "user_name": None,
  # TODO 14: allow the computer to stop the conversation if the user says "goodbye"
  "continue_conversation": True
}

# This variable tracks whether we have a leftover intent from earlier in the
# conversation.
current_intent_name = None

def update_conversation_state_with_value(variable_name, variable_value):
  def update_this_variable():
    conversation_state[variable_name] = variable_value
  return update_this_variable

def update_conversation_state_with_utterance(variable_name):
  def update_this_variable(utterance):
    conversation_state[variable_name] = utterance.strip()
  return update_this_variable

"""
Here's where we store data of what kinds of intentions the user might have in
talking to the chatbot. Things like greetings, farewells, asking for the
chatbot's name, etc.

Right now, we're starting off with just one intent, a "greeting" intent. Each
intent stores patterns of text the user might say that would signal this intent
and some information about how to respond.

TODO 6: add more intents
"""
intents = {
  # Each user intent has a name to identify it, in this case, to greet the
  # chatbot
  "greeting": {
    # Things the user might say that would signal their intent to greet the
    # chatbot
    "utterance_patterns": [
      # TODO 3: this should be a comma-separated list of strings that the user
      # might say that are greetings
      "hello", 
      "good morning", 
      "good afternoon", 
      "good evening",
      "hi", 
      "hey"
    ],
    # Ways the chatbot can respond if the user intends to greet the chatbot
    # TODO 8: add more ways the chatbot can respond to a greeting
    "responses": [
      # {
      #   "text": "Hello!",
      # },
      {
        # Text to send back to the user might require the chatbot to remember
        # things the user has said in the past.
        "text": "Hello there, {user_name}!",
        #TODO 16: ask for the username, if we don't know it yet
        "required_state_variables": ["user_name"]
      }
    ]
  },
  "ask_name": {
    "utterance_patterns": [
      "what's your name?",
      "what is your name?",
      "who are you?",
      "what is your name"
    ],
    "responses": [
      {
        "text": "Hmm, what a good question. I do not know. Might you have any suggestions?",
        "next_intent": "suggest_name"
      }
    ]
  },
  "suggest_name": {
    "utterance_patterns": [
      "your name should be ..."
    ],
    "interpretation_function": update_conversation_state_with_utterance("chatbot_name"),
    "responses": [
      {
        "text": "Thanks, {chatbot_name} is a good name!",
        "required_state_variables": ["chatbot_name"]
      },
      {
        "text": "Thank you, what a lovely name."
      }
    ]
  },
  "ask_age": {
    "utterance_patterns": [
      "How old are you",
      "How old r u"
    ],
    "responses": [
      {
        "text": "That is a good question...a question that I don't know the answer to."
      },
      {
        "text": "I am as old as you would like to think I am."
      }
    ]
  },
    "ask_favorite_foods": {
    "utterance_patterns": [
      "What food do you like?",
      "What's your favorite food?",
      "What do you like to eat?",
      "What's your favorite thing to eat?"
    ],
    "responses": [
      {
        "text": "My favorite food.... Now I'd have to say jalapeños!"
      }
    ]
  },
    "ask_joke": {
    "utterance_patterns": [
      "Tell me a joke",
      "Do you know any jokes?",
      "What's a good joke?"
    ],
    "responses": [
      {
        "text": "Ladies and gents, if he can't appreciate your fruit jokes, you need to let that mango."
      },
      {
        "text": "Why was Dumbo the elephant sad? He felt irrelephant."
      },
      {
        "text": "Why do spiders adapt so quickly to online learning? They're very comfortable on the web."
      },
      {
        "text": "A sheep, a drum, and a snake fell off a cliff. What do you hear? Bah-dum-sss."
      },
    ]
  },
  # TODO 14: modify the ask_riddle intent so that it triggers a next_intent to
  # guess the answer to the riddle.
  # TODO 15: make a new answer_riddle intent and have the chatbot tell the user
  # if they got the right answer using the "riddle_answer" variable in the
  # conversation_state
    "ask_riddle": {
      "utterance_patterns": [
        "Tell me a riddle",
        "Do you have any riddles?",
        "Do you know any riddles?"
        "Give me a riddle"
      ],
      "responses": [
        {
          "text": "Here is an example riddle",
          "response_function": update_conversation_state_with_value(
            # Here's the key for the variable in the conversation state:
            "riddle_answer",
            # Here's the value of that variable (and the answer to the riddle):
            "42"
          )
        }
      ]
    },
    # A default intent. What should we do if we can't understand what the user
    # was trying to say?
    "default": {
      "utterance_patterns": [],
      "responses": [
        {
          "text": "I'm sorry, I did not understand."
        }
      ]
    },
        "end_conversation": {
      "utterance_patterns": [
        "goodbye",
        "good bye",
        "stop",
        "bye"
      ],
      "responses": [
        {
          "text": "Farewell!",
          "response_function": update_conversation_state_with_value(
            "continue_conversation", 
            False
          )
        }
      ]
    }
  # "INTENT_NAME": {
  #   "utterance_patterns": [
  #     "",
  #     ""
  #   ],
  #   "responses": [
  #     {
  #       "text": ""
  #     }
  #   ]
  # }
}

"""
A function that takes in a pattern from the intent and the actual utterance the
user said and decides whether the pattern matches what the user said
TODO 9: improve matching function to ignore case (uppercase vs lowercase)
TODO 10: improve matching function to ignore whitespace
TODO 11: more improvements to matching function?
"""
def match_utterances(utterance, utterance_pattern):
  # TODO 4: check if the utterance is exactly the same as the utterance pattern
  # Let's remove puntuation 
  lower_utterance = utterance.lower().strip() 
  clean_utterance = lower_utterance.translate(str.maketrans('', '', string.punctuation))
  utterance_pattern = utterance_pattern.lower().strip() 
  utterance_pattern = utterance_pattern.translate(str.maketrans('', '', string.punctuation))
  if clean_utterance == utterance_pattern:
    return True
  else:
    return False

"""
Given an utterance from the user, determine what their intention was.

Returns the name of the intent that was matched to the user's utterance
"""
def match_intent(utterance):
  # Look through every intent name in the intents dict
  for intent_name in intents:
    # Grab the dict with data for that intent
    intent = intents[intent_name]
    # Grab the utterance patterns that signal that intent
    utterance_patterns = intent["utterance_patterns"]
    # For each utterance pattern, see if it matches what the
    # user actually said
    for utterance_pattern in utterance_patterns:
      # If a pattern in this intent matches what the user
      # said, then return the name of the intent that
      # was matched.
      if match_utterances(utterance, utterance_pattern):
        return intent_name
  # If we get through all the intents and none of the patterns
  # match, return None to indicate there was no match
  return "default"

"""
Some of the responses the chatbot might consider include information like the
user's name that get's learned through the conversation. If the user hasn't told
the chatbot that information yet, then the chatbot can't use that information
to create the response. So we filter to only the responses that we have enough
information for.
"""
def filter_responses_to_known_variables(responses):
  possible_responses = []
  for response in responses:
    # If the response requires variables from the conversation
    # state, check if we have those variables
    if "required_state_variables" in response:
      required_variables = response["required_state_variables"]
      # Start off assuming that we are NOT missing variables
      missing_variables = False
      for required_variable in required_variables:
        if required_variable in conversation_state:
          if conversation_state[required_variable] is None:
            missing_variables = True
        else:
          # If we find a missing variable, set missing_variables
          # to True
          missing_variables = True
    # If the response doesn't require any variables, then
    # none of the variables are missing
    else:
      missing_variables = False
    if not missing_variables:
      possible_responses.append(response)
  return possible_responses

"""
Given a user's intention, decide how the chatbot should respond.
"""
def decide_response(intent_name):
  # Grab the dict with data for that intent
  intent = intents[intent_name]
  # Grab all possible responses for that intent
  all_responses = intent["responses"]
  # Filter to only the responses we have enough information for
  # (exclude any intents that require more variables in the
  # conversation state)
  possible_responses = filter_responses_to_known_variables(all_responses)
  # TODO 7: randomly chose from multiple possible responses
  response = choice(all_responses)
  # TODO 5: return the first element from possible_responses
  # response = possible_responses[0]
  return response

"""
Display a prompt and return the user's utterance
"""
def get_user_utterance():
  # get input from the user
  user_utterance = input("Type something here to have a chat: ")
  return user_utterance

"""
Once we've decided on the text of our response, print that text out for the user
"""
def display_chatbot_response(response):
  # TODO 2: print out the chatbot's response
  if "chatbot_name" in conversation_state:
    chatbot_name = conversation_state["chatbot_name"]
    print(chatbot_name, ": ", response, sep = "")
  else:
    print("Chat Bot:", response)

"""
Some extra code to add variables that the chatbot remembers from talking to the
user, like the user's name or favorite color.
"""
def add_variables_to_response(response_data):
  text = response_data["text"]
  if "required_state_variables" in response_data:
    required_variables = response_data["required_state_variables"]
    text = text.format(**conversation_state)
  return text

def interpret_utterance(intent_name, utterance):
  intent_data = intents[intent_name]
  if "interpretation_function" in intent_data:
    interpretation_function = intent_data["interpretation_function"]
    interpretation_function(utterance)

def perform_response_action(response_data):
  if "response_function" in response_data:
    response_function = response_data["response_function"]
    response_function()

"""
Before we get to the main loop of the conversation, start off with a predictable
script where the chatbot introduces themselves and asks the user questions
TODO 12: add introduction text where the chatbot introduces themself to the user
TODO 13: ask user's name and put that into the conversation_state (dict at top)
"""
def introduction():
  introductions = """
  This is a chatbot designed to have a friendly conversation with the user. 
  
  For starters, you may like to try asking its name, or telling it yours! Perhaps it will even tell you a joke.
  """
  print(introductions)
  username = input("What is your name?")
  username = username.strip()
  conversation_state["user_name"] = username
"""
Main program loop
"""
def main():
  global current_intent_name

  introduction()

  while conversation_state["continue_conversation"]:
    user_utterance = get_user_utterance()

    # We might have an intent leftover?
    if current_intent_name is None:
      user_intent_name = match_intent(user_utterance)
    else:
      # Once we've used the leftover intent, we reset the "current_intent_name"
      user_intent_name = current_intent_name
      current_intent_name = None

    # Once we know what the user is trying to do, interpret the details of
    # their utterance and save any variables to the conversation_state
    interpret_utterance(user_intent_name, user_utterance)

    chatbot_response_data = decide_response(user_intent_name)

    # We might update current intent based on what the chatbot says
    if "next_intent" in chatbot_response_data:
      current_intent_name = chatbot_response_data["next_intent"]
    
    chatbot_response_text = add_variables_to_response(chatbot_response_data)
    display_chatbot_response(chatbot_response_text)

    # Some responses come with actions, here's an opportunity to do something
    # other than just print text as part of the response
    perform_response_action(chatbot_response_data)

main()