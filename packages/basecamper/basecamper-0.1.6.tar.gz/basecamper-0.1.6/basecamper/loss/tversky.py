import torch
import torch.nn as nn
import torch.nn.functional as F


class TverskyLoss(nn.Module):
    """Computes the Tversky loss [1].
    Args:
        target: a tensor of shape [B, H, W] or [B, 1, H, W].
        predicted: a tensor of shape [B, C, H, W]. Corresponds to
            the raw output or predicted of the model.
        alpha: controls the penalty for false positives.
        beta: controls the penalty for false negatives.
        eps: added to the denominator for numerical stability.
    Returns:
        tversky_loss: the Tversky loss.
    Notes:
        alpha = beta = 0.5 => dice coeff
        alpha = beta = 1 => tanimoto coeff
        alpha + beta = 1 => F beta coeff
    References:
        [1]: https://arxiv.org/abs/1706.05721
    """
    def __init__(self, args):
        super(TverskyLoss, self).__init__()
        self.alpha = args.alpha
        self.beta = args.beta
        self.gpu = args.gpu

        if hasattr(args, 'eps'):
            self.eps = args.eps
        else:
            self.eps = 1e-7

        if hasattr(args, 'size_average'):
            self.size_average = args.size_average
        else:
            self.size_average = True

    def forward(self, predicted, target):
        num_classes = predicted.shape[1]
        if num_classes == 1:
            target_1_hot = torch.eye(num_classes + 1)[target.squeeze(1)]
            target_1_hot = target_1_hot.permute(0, 3, 1, 2).float()
            target_1_hot_f = target_1_hot[:, 0:1, :, :]
            target_1_hot_s = target_1_hot[:, 1:2, :, :]
            target_1_hot = torch.cat([target_1_hot_s, target_1_hot_f], dim=1)
            # pos_prob = torch.sigmoid(predicted) #apply before model output
            neg_prob = 1 - predicted
            probas = torch.cat([predicted, neg_prob], dim=1)
        else:
            target_1_hot = torch.eye(num_classes)[target.squeeze(1)]
            target_1_hot = target_1_hot.permute(0, 3, 1, 2).float()
            # probas = F.softmax(predicted, dim=1) #apply before model

        if self.gpu > -1:
            target_1_hot = target_1_hot.cuda(self.gpu)

        target_1_hot = target_1_hot.type(predicted.type())
        dims = (0,) + tuple(range(2, target.ndimension()))
        intersection = torch.sum(probas * target_1_hot, dims)
        fps = torch.sum(probas * (1 - target_1_hot), dims)
        fns = torch.sum((1 - probas) * target_1_hot, dims)
        num = intersection
        denom = intersection + (self.alpha * fps) + (self.beta * fns)
        tversky_loss = (num / (denom + self.eps)).mean()
        return (1 - tversky_loss)
