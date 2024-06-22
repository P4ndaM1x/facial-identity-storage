import torch
import torchvision
import torchvision.models as models
from torch import nn
from PIL import Image


class ResNetEncoder(torch.nn.Module):
    def __init__(self):
        super(ResNetEncoder, self).__init__()
        original = models.resnet34(weights=models.ResNet34_Weights.DEFAULT)
        self.features = torch.nn.Sequential(*list(original.children())[:-1])

    def forward(self, x):
        x = self.features(x)
        x = torch.flatten(x, 1)
        return x


class EmbeddingExtractor:

    def __init__(self):
        self.transforms = torchvision.transforms.Compose(
            [
                torchvision.transforms.ToPILImage(),
                torchvision.transforms.CenterCrop(224),
                torchvision.transforms.Resize(224),
                torchvision.transforms.ToTensor(),
                torchvision.transforms.Normalize(
                    mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
                ),
            ]
        )
        self.encoder = ResNetEncoder()
        self.result = None

    def vectorize(self, image):
        t_img = self.transforms(image)

        with torch.no_grad():
            res = self.encoder(t_img.unsqueeze(0))
            self.result = res.flatten().tolist()
            return self

    def as_str(self):
        return "[" + ",".join([str(el) for el in self.result]) + "]"

    def get(self):
        return self.result

    def list_from_str(s):
        s = s.strip("[]")
        elements = s.split(",")
        result = [float(el) for el in elements]
        return result
