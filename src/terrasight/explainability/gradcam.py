from __future__ import annotations

import torch
import torch.nn.functional as F
from torch import nn


class GradCAM:
    """Minimal Grad-CAM implementation for CNN models."""

    def __init__(self, model: nn.Module, target_layer: nn.Module) -> None:
        self.model = model
        self.target_layer = target_layer
        self.activations: torch.Tensor | None = None
        self.gradients: torch.Tensor | None = None

        self.forward_hook = target_layer.register_forward_hook(self._save_activations)
        self.backward_hook = target_layer.register_full_backward_hook(self._save_gradients)

    def _save_activations(self, module, inputs, output) -> None:
        self.activations = output.detach()

    def _save_gradients(self, module, grad_input, grad_output) -> None:
        self.gradients = grad_output[0].detach()

    def generate(
        self,
        image: torch.Tensor,
        class_index: int | None = None,
    ) -> torch.Tensor:
        """Generate Grad-CAM heatmap.

        Args:
            image: Tensor with shape [1, C, H, W].
            class_index: Target class. If None, uses predicted class.

        Returns:
            Heatmap tensor with shape [H, W].
        """

        self.model.eval()
        self.model.zero_grad(set_to_none=True)

        logits = self.model(image)

        if class_index is None:
            class_index = int(torch.argmax(logits, dim=1).item())

        score = logits[:, class_index].sum()
        score.backward()

        if self.activations is None or self.gradients is None:
            raise RuntimeError("Grad-CAM hooks did not capture activations/gradients.")

        weights = self.gradients.mean(dim=(2, 3), keepdim=True)
        cam = torch.sum(weights * self.activations, dim=1, keepdim=True)
        cam = F.relu(cam)

        cam = F.interpolate(
            cam,
            size=image.shape[-2:],
            mode="bilinear",
            align_corners=False,
        )

        cam = cam.squeeze()

        cam_min = cam.min()
        cam_max = cam.max()

        if cam_max > cam_min:
            cam = (cam - cam_min) / (cam_max - cam_min)

        return cam.detach().cpu()

    def close(self) -> None:
        """Remove hooks."""

        self.forward_hook.remove()
        self.backward_hook.remove()


def get_resnet_target_layer(model: nn.Module) -> nn.Module:
    """Return default Grad-CAM target layer for torchvision ResNet."""

    if not hasattr(model, "layer4"):
        raise ValueError("Model does not have layer4. Provide target layer manually.")

    return model.layer4[-1]