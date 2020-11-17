import json
import logging
import random
import numpy
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

from bot.utils import NaturalLangProcessor
from bot.net.models import NeuralNet


logger = logging.getLogger(__name__)


def start_training(intents, epochs):
    nlp = NaturalLangProcessor()

    try:
        all_words, tags, xy = parse_intents(intents, nlp)
    except LookupError as e:
        logger.warning('punkt package missing, downloading...')
        nlp.dl_punkt()
        logger.warning('punkt downloaded, trying again...')
        all_words, tags, xy = parse_intents(intents, nlp)

    trained_x, trained_y = train_xy(all_words, tags, xy, nlp)
    model_data = train_main(trained_x, trained_y, tags, all_words, epochs)
    return model_data


def parse_intents(intents, nlp):
    all_words = []
    tags = []
    xy = []
    ignore_chars = ["?", "!", ".", ",", "'"]
    for intent in intents['intents']:
        tag = intent['tag']
        tags.append(tag)
        for pattern in intent['patterns']:
            w = nlp.tokenize(pattern)
            all_words.extend(w)
            xy.append((w, tag))

    all_words = [nlp.stem(w) for w in all_words if w not in ignore_chars]
    all_words = sorted(set(all_words))
    tags = sorted(set(tags))
    return all_words, tags, xy


def train_xy(all_words, tags, xy, nlp):
    '''
    Create bags of words for the patterns
    '''
    x_train = []
    y_train = []
    for (pattern, tag) in xy:
        bag = nlp.bag_of_words(pattern, all_words)
        x_train.append(bag)
        label = tags.index(tag)
        y_train.append(label)

    x_train = numpy.array(x_train)
    y_train = numpy.array(y_train)

    return x_train, y_train


def train_main(x_train, y_train, tags, all_words, epochs):
    batch = 8
    hidden_size = 8
    output_size = len(tags)
    # length of each bag of words/all_words (first bag of words in this case)
    input_size = len(x_train[0])
    learning_rate = 0.001
    num_epochs = epochs

    data = ChatDataset(x_train, y_train)
    train_loader = DataLoader(
        dataset=data,
        batch_size=batch,
        shuffle=True,
        num_workers=0
    )

    device = 'cpu'
    model = NeuralNet(input_size, hidden_size, output_size).to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

    for epoch in range(num_epochs):
        for (words, labels) in train_loader:
            words = words.to(device)
            labels = labels.to(device)

            # predicted outputs
            outputs = model(words)
            loss = criterion(outputs, labels)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        if (epoch+1) % 100 == 0:
            logger.warning(
                f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')

    logger.warning(f'Training complete, final loss: {loss.item():.4f}')

    rating = ''
    if loss.item() > 0.005:
        rating = 'not too great'
    elif 0.005 > loss.item() > 0.002:
        rating = 'ok'
    elif 0.002 > loss.item() > 0.0002:
        rating = 'good'
    else:
        rating = 'very good'

    data = {
        "final_loss": loss.item(),
        "training_rating": rating,
        "model_state": model.state_dict(),
        "optimizer_state": optimizer.state_dict(),
        "input_size": input_size,
        "hidden_size": hidden_size,
        "output_size": output_size,
        "all_words": all_words,
        "tags": tags,
    }
    FILE = "data.pth"
    torch.save(data, FILE)

    return data


class ChatDataset(Dataset):
    def __init__(self, x_train, y_train):
        self.n_samples = len(x_train)
        self.x_data = x_train
        self.y_data = y_train

    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    def __len__(self):
        return self.n_samples
