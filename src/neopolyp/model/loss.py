import torch
from torch import Tensor


def dice_score(
    logits: Tensor,
    target: Tensor,
    smooth: float = 1e-6
):
    # Average of Dice coefficient for all batches, or for a single mask
    inputs = torch.softmax(logits, dim=1)

    # flatten label and prediction tensors
    inputs = inputs.reshape(-1)
    targets = target.reshape(-1)

    intersection = (inputs * targets).sum()
    dice = 2.*(intersection + smooth)/(inputs.sum() + targets.sum() + smooth)

    return dice


def dice_loss(
    logits: Tensor,
    target: Tensor,
    epsilon: float = 1e-6
):
    return 1 - dice_score(logits, target, epsilon)


def focal_tversky_loss(
    logits: Tensor,
    targets: Tensor,
    smooth: float = 1e-6,
    alpha: float = 0.5,
    beta: float = 0.5,
    gamma: float = 1
):

    # flatten label and prediction tensors
    logits = logits.reshape(-1)
    targets = targets.reshape(-1)

    # True Positives, False Positives & False Negatives
    TP = (logits * targets).sum()
    FP = ((1-targets) * logits).sum()
    FN = (targets * (1-logits)).sum()

    tversky = (TP + smooth) / (TP + alpha*FP + beta*FN + smooth)
    focal_tversky = (1 - tversky)**gamma

    return focal_tversky


if __name__ == "__main__":
    a = torch.rand(4, 3, 8, 8)
    b = torch.randint(0, 2, (4, 3, 8, 8))
    print(dice_loss(a, b))
    print(focal_tversky_loss(a, b))
