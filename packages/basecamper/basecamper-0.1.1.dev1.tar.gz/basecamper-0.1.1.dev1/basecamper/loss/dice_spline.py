import torch.nn as nn

from .dice import DiceLoss
from .spline import SplineLoss


class DiceSplineLoss(nn.Module):
    """Computes the DiceSpline loss.

    Weighted combination of dice and spline loss.
    Args:
        target: a tensor of shape [B, 1, H, W].
        predicted: a tensor of shape [B, C, H, W]. Corresponds to
            the raw output or predicted of the model.
    Returns:
        dice_spline_loss: the DiceSpline loss.
    """

    def __init__(self, args):
        super(DiceSplineLoss, self).__init__()
        self.gpu = args.gpu
        self.patch_size = args.input_shape[2]

        if hasattr(args, 'eps'):
            self.eps = args.eps
        else:
            self.eps = 1e-7

        self.dice = DiceLoss(args)
        self.spline = SplineLoss(args)
        self.alpha = args.dice_spline_cntrl

    def forward(self, predicted, target):
        """Compute loss between :attr:`predicted` and :attr:`target`.

        Parameters
        ----------
        predicted : torch.Tensor
            Predicted output tensor from a model.
        target : torch.Tensor
            Ground truth tensor.

        Returns
        -------
        torch.Tensor
            DiceSpline loss computed between :attr:`predicted` and
            :attr:`target`.

        """
        return (1 - self.alpha) * self.dice(predicted, target) + \
            self.alpha * self.spline(predicted, target)
