import random
import json

import torch

import comp_stat

from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

bot_name = "Sam"
department='NULL'
subject='NULL'

print("--WELCOME to complaint registration system (type 'quit' to exit)--")
print(f"{bot_name}:How may I help you?")


while True:

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    with open('intents.json', 'r') as json_data:
        intents = json.load(json_data)

    FILE = "data.pth"
    data = torch.load(FILE)

    input_size = data["input_size"]
    hidden_size = data["hidden_size"]
    output_size = data["output_size"]
    all_words = data['all_words']
    tags = data['tags']
    model_state = data["model_state"]

    model = NeuralNet(input_size, hidden_size, output_size).to(device)
    model.load_state_dict(model_state)
    model.eval()

    # sentence = "do you use credit cards?"
    sentence = input("You: ")
    if sentence == "quit":
        break

    # identifying customer intent(register/status/reminder)    
    sentence = tokenize(sentence)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:    #intent found

        if tag == "greeting":
            print(f"{bot_name}:Hey!How may I help you?")

        if tag == "goodbye":
            print(f"{bot_name}:See you later.Thanks for visiting")
            break

        if tag == "thanks":
            print(f"{bot_name}:Happy to help, come back anytime")
            break

        if tag == "register":      
                print(f"{bot_name}:Do you want to register a new complaint? Y/N")
                ans=input('You:')
                if ans == "Y":
                    print(f"{bot_name}:Please type in your complaint")
                    for y in range(2): #Max two tries to identify subject and department
                        sentence=input("You:") 
                        # department='NULL'
                        # subject='NULL'

                        if subject == 'NULL':
                            #finding subject
                            device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

                            FILE = "data1.pth"
                            data = torch.load(FILE)

                            input_size = data["input_size"]
                            hidden_size = data["hidden_size"]
                            output_size = data["output_size"]
                            all_words = data['all_words']
                            tags = data['tags']
                            model_state = data["model_state"]

                            model = NeuralNet(input_size, hidden_size, output_size).to(device)
                            model.load_state_dict(model_state)
                            model.eval()

                            sentence_1 = tokenize(sentence)
                            X = bag_of_words(sentence_1, all_words)
                            X = X.reshape(1, X.shape[0])
                            X = torch.from_numpy(X).to(device)

                            output = model(X)
                            _, predicted = torch.max(output, dim=1)

                            tag = tags[predicted.item()]

                            probs = torch.softmax(output, dim=1)
                            prob = probs[0][predicted.item()]
                            if prob.item() > 0.75:
                                subject = tag

                        if department == 'NULL':
                            #finding department
                            FILE = "data2.pth"
                            data = torch.load(FILE)
                            input_size = data["input_size"]
                            hidden_size = data["hidden_size"]
                            output_size = data["output_size"]
                            all_words = data['all_words']
                            tags = data['tags']
                            model_state = data["model_state"]
                            model = NeuralNet(input_size, hidden_size, output_size).to(device)
                            model.load_state_dict(model_state)
                            model.eval()

                            sentence_2 = tokenize(sentence)
                            X = bag_of_words(sentence_2, all_words)
                            X = X.reshape(1, X.shape[0])
                            X = torch.from_numpy(X).to(device)

                            output = model(X)
                            _, predicted = torch.max(output, dim=1)

                            tag = tags[predicted.item()]

                            probs = torch.softmax(output, dim=1)
                            prob = probs[0][predicted.item()]
                            if prob.item() > 0.75:
                                department = tag

                        if subject != 'NULL' and department !='NULL':
                            #register complaint
                            print(f"{bot_name}:Complaint registered successfully")
                            print(f"{bot_name}:Is there anything else I can help you with?")
                            break
                        else:
                            if y==0:
                                #couldnt find subject &OR department in first try
                                print(f"{bot_name}:Please rephrase your complaint")
                            elif y==1:
                                #couldnt understand subject &OR department in second try
                                #register without subject &OR department
                                print(f"{bot_name}:Complaint registered successfully")
                                print(f"{bot_name}:Is there anything else I can help you with?")

                elif ans == "N":
                    print(f"{bot_name}:Will you please clarify how may I help you?")
                    
                else:
                    print(f"{bot_name}:Please enter Y/N")

        if tag == "status" :
            print(f"{bot_name}:Do you want to know the status of an existing complaint? Y/N")
            ans=input('You:')
            if ans == "Y":
                print(f"{bot_name}:please enter your complaint id") 
                griev_id=input("You:") 
                print(f"{bot_name}: Complaint status-",end='')
                print(comp_stat.checkstat(griev_id))
                print(f"{bot_name}:Is there anything else I can help you with?")
            elif ans == "N":
                print(f"{bot_name}:Will you please clarify how may I help you?")
                    
        if tag == "reminder":

            print(f"{bot_name}:Do you want to set reminder for existing complaint? Y/N")
            ans=input('You:')

            if ans == "Y":        
                print(f"{bot_name}:please enter your complaint id") 
                griev_id=input("You:") 
                print(f"{bot_name}:",end=' ')
                comp_stat.setrem(griev_id)
                print(f"{bot_name}:Is there anything else I can help you with?")
            
            elif ans == "N":
                print(f"{bot_name}:Will you please clarify how may I help you?")
                    
            else:
                print(f"{bot_name}:Please enter Y/N")


              
    else:
        print(f"{bot_name}: I do not understand...")
        #we can present a menu containing register status and reminder in place of this msg 

print("---Thanks for using our services---")
print (subject)
print(department)