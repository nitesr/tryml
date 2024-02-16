from torchvision import models
from torch import nn, argmax

class TinyImageNet(nn.Module):
    def __init__(self, num_classes=10) -> None:
        super(TinyImageNet, self).__init__()
        self.backbone = models.resnet152()
        self.backbone._modules['fc'] = nn.Linear(in_features=2048, out_features=10, bias=True)
    
    def forward(self, X):
        return self.backbone(X)
    
    def predict(self, X):
        logits = self.forward(X)
        return argmax(logits, 1)
    
    