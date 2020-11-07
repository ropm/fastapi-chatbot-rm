import random
import json

import torch

from bot.net.models import NeuralNet
from bot.utils import NaturalLangProcessor


def start_chatting(message):
    with open('intents.json', 'r') as f:
        intents = json.load(f)
    nlp = NaturalLangProcessor()

    device = 'cpu'
    FILE = 'data.pth'
    data = torch.load(FILE)
    model = NeuralNet(data['input_size'],
                      data['hidden_size'], data['output_size']).to(device)
    model.load_state_dict(data['model_state'])
    model.eval()

    message = nlp.tokenize(message)
    X = nlp.bag_of_words(message, data['all_words'])
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = data['tags'][predicted.item()]

    all_probs = torch.softmax(output, dim=1)
    prob = all_probs[0][predicted.item()]

    response = 'Sorry, I could not understand... :('

    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent['tag']:
                response = random.choice(intent['responses'])

    return response
