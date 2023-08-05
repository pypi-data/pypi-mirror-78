import torch
import torch.nn as nn


class SplineLoss(nn.Module):
    """Computes the Spline loss.

    AKA Active Contour Loss from https://ieeexplore.ieee.org/document/8953484
    Args:
        target: a tensor of shape [B, 1, H, W].
        predicted: a tensor of shape [B, C, H, W]. Corresponds to
            the raw output or predicted of the model.
    Returns:
        spline_loss: the Spline loss.
    """

    def __init__(self, args):
        super(SplineLoss, self).__init__()
        self.patch_size = args.input_shape[2]
        self.gpu = args.gpu

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
            Spline loss computed between :attr:`predicted` and :attr:`target`.

        """
        predicted = predicted.float()
        target = target.float()

        # horizontal and vertical directions
        x = predicted[:, 1:, :] - predicted[:, :-1, :]
        y = predicted[:, :, 1:] - predicted[:, :, :-1]

        delta_x = x[:, 1:, :-2]**2
        delta_y = y[:, :-2, 1:]**2
        delta_u = torch.abs(delta_x + delta_y)

        # where is a parameter to avoid square root is zero in practice.
        epsilon = 0.00000001
        w = 1
        # equ.(11) in the paper
        length = w * torch.sum(torch.sqrt(delta_u + epsilon))

        c_1 = torch.ones((self.patch_size, self.patch_size))
        c_2 = torch.zeros((self.patch_size, self.patch_size))
        if self.gpu > -1:
            c_1 = c_1.cuda(self.gpu)
            c_2 = c_2.cuda(self.gpu)

        region_in = torch.abs(
                        torch.sum(
                            predicted[:, :, :] * ((target[:, :, :] - c_1)**2)
                        )
                    )  # equ.(12) in the paper
        region_out = torch.abs(
                        torch.sum(
                         (1-predicted[:, :, :]) * ((target[:, :, :] - c_2)**2)
                        )
                     )  # equ.(12) in the paper

        lambda_p = 1  # lambda parameter could be various.

        loss = length + lambda_p * (region_in + region_out)

        return loss
