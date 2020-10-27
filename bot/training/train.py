import json
import logging
import random
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

from bot.utils import NaturalLangProcessor
from bot.net.models import NeuralNet


logger = logging.getLogger(__name__)

class Trainer:
    def __init__(self):
        self.file = open('intents.json', 'r'):
        self.intents = json.load(file)
        self.all_words = []
        self.tags = []
        self.xy = []
        self.processor = NaturalLangProcessor()

    def setup_training_data(self):
        ignored_chars = ['?', '!', '.']
        for intent in self.intents['intents']:
            tag = intent['tag']
            self.tags.append(tag)
            for pattern in intents['patterns']:
                w = self.processor.tokenize(pattern)
                self.all_words.extend(w)
                self.xy.append((w, tag))
        self.all_words = [self.processor.stem(w) for w in self.all_words if w not in ignored_chars]
        self.all_words = sorted(set(self.all_words))
        self.tags = sorted(set(self.tags))
        logger.debug(f'Patterns: {len(self.xy)}')
        logger.debug(f'Tags count: {len(self.tags)}, tags: {self.tags}')
        logger.debug(f'Stemmed words count: {len(self.all_words)}, words: {self.all_words}')

    def create_training_data(self):
        # create training data
        X_train = []
        y_train = []
        for (pattern_sentence, tag) in xy:
            # X: bag of words for each pattern_sentence
            bag = bag_of_words(pattern_sentence, all_words)
            X_train.append(bag)
            # y: PyTorch CrossEntropyLoss needs only class labels, not one-hot
            label = tags.index(tag)
            y_train.append(label)

        X_train = np.array(X_train)
        y_train = np.array(y_train)

        # Hyper-parameters 
        num_epochs = 1000
        batch_size = 8
        learning_rate = 0.001
        input_size = len(X_train[0])
        hidden_size = 8
        output_size = len(tags)
        print(input_size, output_size)

class ChatDataset(Dataset):

    def __init__(self):
        self.n_samples = len(X_train)
        self.x_data = X_train
        self.y_data = y_train

    # support indexing such that dataset[i] can be used to get i-th sample
    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    # we can call len(dataset) to return the size
    def __len__(self):
        return self.n_samples

dataset = ChatDataset()
train_loader = DataLoader(dataset=dataset,
                          batch_size=batch_size,
                          shuffle=True,
                          num_workers=0)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = NeuralNet(input_size, hidden_size, output_size).to(device)

# Loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

# Train the model
for epoch in range(num_epochs):
    for (words, labels) in train_loader:
        words = words.to(device)
        labels = labels.to(dtype=torch.long).to(device)
        
        # Forward pass
        outputs = model(words)
        # if y would be one-hot, we must apply
        # labels = torch.max(labels, 1)[1]
        loss = criterion(outputs, labels)
        
        # Backward and optimize
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
    if (epoch+1) % 100 == 0:
        print (f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')


print(f'final loss: {loss.item():.4f}')

data = {
"model_state": model.state_dict(),
"input_size": input_size,
"hidden_size": hidden_size,
"output_size": output_size,
"all_words": all_words,
"tags": tags
}

FILE = "data.pth"
torch.save(data, FILE)

print(f'training complete. file saved to {FILE}')