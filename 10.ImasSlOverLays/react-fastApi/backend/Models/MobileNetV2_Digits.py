# Models/MobileNetV2_Digits.py
import os
import cv2
import torch
import torch.nn as nn
from torchvision import models, transforms

# MobileNetV2モデルの定義
class MobileNetV2_Digits:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model, self.labels = self._load_model_and_labels()

    def _load_model_and_labels(self):
        # モデルパスを自身のパスから相対パスで指定
        model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'MobileNetV2_Digits.pth')
        checkpoint = torch.load(model_path, map_location=self.device)
        
        model = models.mobilenet_v2(weights=None)
        model.features[0][0] = nn.Conv2d(1, model.features[0][0].out_channels, kernel_size=3, stride=2, padding=1, bias=False)
        model.classifier[1] = nn.Linear(model.last_channel, len(checkpoint['label_mapping']))
        model.load_state_dict(checkpoint['model_state_dict'])
        model.to(self.device)
        model.eval()
        
        return model, checkpoint['label_mapping']

    def _resize_and_binarize(self, image):
        height, width = image.shape
        aspect_ratio = width / height
        new_width = int(65 * aspect_ratio)
        resized_image = cv2.resize(image, (new_width, 65), interpolation=cv2.INTER_LANCZOS4)
        _, binary_image = cv2.threshold(resized_image, 128, 255, cv2.THRESH_BINARY)
        return binary_image

    def predict(self, image):
        image = self._resize_and_binarize(image)
        image = self.transform(image).unsqueeze(0).to(self.device)
        with torch.no_grad():
            output = self.model(image)
            _, predicted = torch.max(output, 1)
            return self.labels[predicted.item()]

    @property
    def transform(self):
        return transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize((65, 40)),
            transforms.ToTensor(),
            transforms.Normalize((0.5,), (0.5,))
        ])