from torchvision import transforms
from torchvision import models
import torch


class Model():
    def __init__(self):
        self.efficientnet_v2_s = models.efficientnet_v2_s(pretrained=True)
        self.efficientnet_v2_s.eval()

        self.transform = transforms.Compose([transforms.ToPILImage(),
                                             transforms.Resize(256),
                                             transforms.CenterCrop(224),
                                             transforms.ToTensor(),
                                             transforms.Normalize(
                                             mean=[0.485, 0.456, 0.406],
                                             std=[0.229, 0.224, 0.225])])

    def check_similarity(self, image):
        image_tensor = torch.unsqueeze(self.transform(image), 0)
        out = self.efficientnet_v2_s(image_tensor)
        similarity = torch.nn.functional.softmax(out, dim=1)[0] * 100
        swansim = similarity[100].item()
        return swansim
