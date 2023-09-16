import json
import string
import random
import nltk
import numpy as num
from nltk.stem import WordNetLemmatizer # It has the ability to lemmatize.
import tensorflow as tensorF # A multidimensional array of elements is represented by this symbol.
from tensorflow.keras import Sequential # Sequential groups a linear stack of layers into a tf.keras.Model
from tensorflow.keras.layers import Dense, Dropout
# from chatbotContent import data
nltk.download("punkt")# required package for tokenization
nltk.download("wordnet")# word database
from spellchecker import SpellChecker
from nltk.tag import pos_tag
from .models import User


def chatbot_func(newMessage, data, dataframe_pattern_words, ourClasses, ourNewModel):
    pass
    spell = SpellChecker()
    def lemmatize_word(token):
        pos_tag_word = pos_tag([token])[0][1]
        lemmatizer = WordNetLemmatizer()
        if pos_tag_word.lower()[0] == 'v':
            return lemmatizer.lemmatize(token, pos='v')
        elif pos_tag_word.lower()[0] == 'n':
            return lemmatizer.lemmatize(token, pos='n')  
        else:
            return lemmatizer.lemmatize(token, pos='a')
    def ourText(text):
        newtkns = nltk.word_tokenize(text)
        newtkns = [lemmatize_word(word) for word in newtkns]
        print(newtkns,"=====newtkns======")
        return newtkns

    def wordBag(newMessage_no_punc, dataframe_pattern_words, length_input):
        newtkns = newMessage_no_punc
        bagOwords = [0] * len(dataframe_pattern_words)
        for w in newtkns:
            # for idx, word in enumerate(dataframe_pattern_words):
            if w in dataframe_pattern_words:
                bagOwords[dataframe_pattern_words.index(w)] = 1    
            else:
                if correct_spelling(w) in dataframe_pattern_words:
                    bagOwords[dataframe_pattern_words.index(correct_spelling(w))] = 1
                else:    
                    print(f'sorry i dont know about the word {w} in your sentence.')        
        print(bagOwords.count(1), '******************bagOwords*******************')
        if bagOwords.count(1) != length_input:
            pass
        return num.array(bagOwords)

    def correct_spelling(text):
        corrected_words = spell.correction(text)
        return corrected_words

    def Pclass(newMessage_no_punc, dataframe_pattern_words, labels, length_input):
        bagOwords = wordBag(newMessage_no_punc, dataframe_pattern_words, length_input)
        ourResult = ourNewModel.predict(num.array([bagOwords]))[0]
        print([i for i in ourResult], '===================ourResult===================')
        newThresh = 0.85
        yp = [[idx, res] for idx, res in enumerate(ourResult) if res > newThresh]
        if not yp: return ['notKnown']
        yp.sort(key=lambda x: x[1], reverse=True)
        newList = []
        for r in yp:
            newList.append(labels[r[0]])
        return newList

    def getRes(firstlist, fJson):
        tag = firstlist[0]
        listOfIntents = fJson["intents"]
        for i in listOfIntents:
            if i["tag"] == tag:
                ourResult = random.choice(i["responses"])
                break
        global previous_msg     
        previous_msg = newMessage    
        return ourResult

    if not newMessage:
        return "Bot:", "please type something"

    if newMessage == "wrong":
        print("Sorry for my wrong answer. Please tell which category this question belongs to")
        categories = [i["tag"] for i in data['intents']]
        categories = {i:j for i,j in enumerate(categories)} 
        new_or_existing = input(f"Type '1'-(for creating new category) '2'-existing category: ")
        if new_or_existing == "2":
            category = input(f"Please tell category from the list {categories} so that I will update in my dataset: ")
            (data["intents"][int(category)]["patterns"]).append(previous_msg)
            with open('chatbotContent.py', 'w', encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
    
    elif newMessage != "wrong":
        newMessage_tokenize = nltk.word_tokenize(newMessage)
        newMessage_no_punc = [lemmatize_word(word.lower()) for word in newMessage_tokenize if word not in string.punctuation]
        if newMessage_no_punc[0][:2] == "hi": newMessage_no_punc[0] = newMessage_no_punc[0][:2]
        if newMessage_no_punc[0][:3] == "hai": newMessage_no_punc[0] = newMessage_no_punc[0][:3]
        intents = Pclass(newMessage_no_punc, dataframe_pattern_words, ourClasses, len(newMessage_no_punc))
        ourResult = getRes(intents, data)
        return ourResult

def train_data(data):
    pass
    with open('api/chatbotContent.py', 'r', encoding="utf-8") as file:
    
        data = json.load(file)

    def lemmatize_word(token):
        pos_tag_word = pos_tag([token])[0][1]
        lemmatizer = WordNetLemmatizer()
        if pos_tag_word.lower()[0] == 'v':
            return lemmatizer.lemmatize(token, pos='v')
        elif pos_tag_word.lower()[0] == 'n':
            return lemmatizer.lemmatize(token, pos='n')  
        else:
            return lemmatizer.lemmatize(token, pos='a')
    # lists
    ourClasses = []
    dataframe_pattern_words = []
    documentX = []
    documentY = []
    # Each intent is tokenized into words and the patterns and their associated tags are added to their respective lists.
    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            ournewTkns = nltk.word_tokenize(pattern)# tokenize the patterns
            dataframe_pattern_words.extend(ournewTkns)# extends the tokens
            documentX.append(pattern)
            documentY.append(intent["tag"])

        if intent["tag"] not in ourClasses:# add unexisting tags to their respective classes
            ourClasses.append(intent["tag"])
    dataframe_pattern_words = [lemmatize_word(word.lower()) for word in dataframe_pattern_words if word not in string.punctuation] # set words to lowercase if not in punctuation
    dataframe_pattern_words = sorted(set(dataframe_pattern_words))# sorting words
    ourClasses = sorted(set(ourClasses))# sorting classes

    trainingData = [] # training list array
    outEmpty = [0] * len(ourClasses)
    # bow model
    for idx, doc in enumerate(documentX):
        bagOfwords = []
        text = lemmatize_word(doc.lower())
        for word in dataframe_pattern_words:
            bagOfwords.append(1) if word in text else bagOfwords.append(0)

        outputRow = list(outEmpty)
        outputRow[ourClasses.index(documentY[idx])] = 1
        trainingData.append([bagOfwords, outputRow])
    random.shuffle(trainingData)
    trainingData = num.array(trainingData, dtype=object)# coverting our data into an array afterv shuffling

    x = num.array(list(trainingData[:, 0]))# first trainig phase
    y = num.array(list(trainingData[:, 1]))# second training phase

    iShape = (len(x[0]),)
    oShape = len(y[0])
    # parameter definition
    ourNewModel = Sequential()
    # In the case of a simple stack of layers, a Sequential model is appropriate

    # Dense function adds an output layer
    ourNewModel.add(Dense(128, input_shape=iShape, activation="relu"))
    # The activation function in a neural network is in charge of converting the node's summed weighted input into activation of the node or output for the input in question
    ourNewModel.add(Dropout(0.5))
    # Dropout is used to enhance visual perception of input neurons
    ourNewModel.add(Dense(64, activation="relu"))
    ourNewModel.add(Dropout(0.3))
    ourNewModel.add(Dense(oShape, activation = "softmax"))
    # below is a callable that returns the value to be used with no arguments   decay=1e-6
    md = tensorF.keras.optimizers.Adam(learning_rate=0.01)
    # Below line improves the numerical stability and pushes the computation of the probability distribution into the categorical crossentropy loss function.
    ourNewModel.compile(loss='categorical_crossentropy', optimizer=md, metrics=["accuracy"])
    # Output the model in summary
    # print(ourNewModel.summary())
    # Whilst training your Nural Network, you have the option of making the output verbose or simple.
    ourNewModel.fit(x, y, epochs=200, verbose=1)     
    return (data, dataframe_pattern_words, ourClasses, ourNewModel)





def get_all_chats(user1):
    user = User.objects.all()
    all_chats = []
    for i in user:
        if i.id == user1 or i.is_superuser == True:
            pass
        else:
            if user1 < i.id:
                all_chats.append({'link':f'https://45e6-112-196-43-19.ngrok-free.app/user/chatting/{user1}/{i.id}/', 'email':i.email})
            elif user1 > i.id:
                all_chats.append({'link':f'https://45e6-112-196-43-19.ngrok-free.app/user/chatting/{i.id}/{user1}/', 'email':i.email})
    return all_chats