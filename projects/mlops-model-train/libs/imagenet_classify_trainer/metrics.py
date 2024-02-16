import torch

def accuracy_fn(logits, y_true):
    y_pred = torch.argmax(logits, 1)
    num_correct = torch.sum(y_pred == y_true).item()
    value = num_correct / len(y_true)
    return value