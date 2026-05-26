import torch
from torch import nn


class NeuralNetwork(nn.Module):
    def __init__(self, features, hidden_one, hidden_two, output=2):

        super().__init__()
        self.features = features
        self.hidden_one = hidden_one
        self.hidden_two = hidden_two
        self.output = output


    def create(self):
        self.model = nn.Sequential(
            nn.Linear(self.features, self.hidden_one),
            nn.ReLU(),
            nn.Linear(self.hidden_one, self.hidden_two),
            nn.ReLU(),
            nn.Linear(self.hidden_two, self.output),
            # nn.Softmax(),
        )

    def configure(self, loss_function=nn.CrossEntropyLoss(), learning_rate=1e-3, weight_decay=1e-2):

        self.loss_function = loss_function
        self.optimiser = torch.optim.AdamW(params=self.model.parameters(), lr=learning_rate, weight_decay=weight_decay)
    
    
    def forward(self, x):

        probs = self.model(x)
        return probs


    def train(self, epochs, X_train, y_train):

        self.model.train()
        for epoch in range(epochs):

            y_pred = self.model(X_train)
            loss = self.loss_function(y_pred, y_train)

            loss.backward()
            self.optimiser.step()
            self.optimiser.zero_grad()


    def predict(self, X_test):

        self.model.eval()
        logits = self.model(X_test)
        y_pred = nn.Softmax()(logits)

        return y_pred

