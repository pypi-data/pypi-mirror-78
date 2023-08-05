import torch
import torch.nn as nn
from torch.autograd import Variable


class FocalLoss(nn.Module):
    r"""Focal loss from https://arxiv.org/pdf/1708.02002.pdf.

    A factor of :math:`(1-\rho_t)^{\gamma}` is added to the
    standard cross entropy criterion. Setting :math:`\gamma>0`
    reduces the relative loss for well-classified examples
    :math: `(\rho_t > 0.5)`, putting more focus on hard, misclassified
    examples.

    Parameters
    ----------
    args : basecamper.grain.grain.Grain
        Arguments passed via the experiment when loss function is called.
        :attr:`args` should contain :attr:`gamma` and :attr:`alpha`.
        :attr:`size_average` is optional.
    Attributes
    ----------
    gamma : float
        Tunable focusing parameter, :math:`\gamma >= 0`.
    alpha : float
        Weighthing factor :math:`\alpha \epsilon [0,1]`.
    size_average : bool
        By default, the losses are averaged over each loss element in the
        batch. Note that for some losses, there are multiple elements per
        sample. If the field :attr:`size_average` is set to ``False``,
        the losses are instead summed for each minibatch. Ignored when reduce
        is ``False``. Default: ``True``

    """

    def __init__(self, args):
        super(FocalLoss, self).__init__()
        self.gamma = args.gamma
        self.alpha = args.alpha
        if isinstance(self.alpha, (float, int)):
            self.alpha = torch.Tensor([self.alpha, 1-self.alpha])
        if isinstance(self.alpha, list):
            self.alpha = torch.Tensor(self.alpha)

        if hasattr(args, 'size_average'):
            self.size_average = args.size_average
        else:
            self.size_average = True

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
            Focal loss computed between :attr:`predicted` and :attr:`target`.

        """
        predicted = predicted.float()
        target = target.long()

        if predicted.dim() > 2:
            predicted = predicted.view(predicted.size(0),
                                       predicted.size(1),
                                       -1)
            predicted = predicted.transpose(1, 2)
            predicted = predicted.contiguous().view(-1, predicted.size(2))

        target = target.view(-1, 1)

        logpt = predicted.gather(1, target)
        logpt = logpt.view(-1)
        pt = Variable(logpt.data.exp())

        if self.alpha is not None:
            if self.alpha.type() != predicted.data.type():
                self.alpha = self.alpha.type_as(predicted.data)
            at = self.alpha.gather(0, target.data.view(-1))
            logpt = logpt * Variable(at)

        loss = -1 * (1 - pt) ** self.gamma * logpt

        if self.size_average:
            return loss.mean()
        else:
            return loss.sum()
