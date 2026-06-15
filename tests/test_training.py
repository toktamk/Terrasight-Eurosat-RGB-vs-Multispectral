import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


import torch

from terrasight.models.rgb_model import build_rgb_model
from terrasight.training.losses import build_loss
from terrasight.training.optimizer_factory import build_optimizer
from terrasight.training.scheduler_factory import build_scheduler


def test_build_cross_entropy_loss() -> None:
    loss = build_loss("cross_entropy")
    assert isinstance(loss, torch.nn.CrossEntropyLoss)


def test_build_optimizer() -> None:
    model = build_rgb_model(pretrained=False)
    optimizer = build_optimizer(
        model=model,
        name="adamw",
        learning_rate=0.001,
        weight_decay=0.0,
    )

    assert isinstance(optimizer, torch.optim.AdamW)


def test_build_scheduler_none() -> None:
    model = build_rgb_model(pretrained=False)
    optimizer = build_optimizer(model=model)

    scheduler = build_scheduler(
        optimizer=optimizer,
        name=None,
        epochs=2,
    )

    assert scheduler is None


def test_single_training_step() -> None:
    model = build_rgb_model(pretrained=False)
    criterion = build_loss("cross_entropy")
    optimizer = build_optimizer(model=model)

    x = torch.randn(2, 3, 64, 64)
    y = torch.tensor([0, 1])

    logits = model(x)
    loss = criterion(logits, y)

    optimizer.zero_grad(set_to_none=True)
    loss.backward()
    optimizer.step()

    assert loss.item() > 0