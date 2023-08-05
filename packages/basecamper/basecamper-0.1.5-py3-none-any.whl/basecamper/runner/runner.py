from torch.autograd import Variable

from basecamper.metrics.metrics import Metrics


class Runner():
    def __init__(self,
                 model,
                 optimizer,
                 criterion,
                 train_loader,
                 val_loader,
                 args,
                 polyaxon_exp=None):
        self.polyaxon_exp = polyaxon_exp
        self.gpu = args.gpu
        self.model = model
        self.optimizer = optimizer
        self.criterion = criterion
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.train_metrics = Metrics(polyaxon_exp=polyaxon_exp,
                                     phase='train',
                                     metrics_strings=args.metrics)
        self.val_metrics = Metrics(polyaxon_exp=polyaxon_exp,
                                   phase='val',
                                   metrics_strings=args.metrics)
        self.epoch = 0

    def set_epoch_metrics(self):
        self.train_metrics.reset()
        self.val_metrics.reset()
        self.epoch += 1

    def tensorize_batch(self, input_tensor, label_tensor):
        input_tensor = Variable(input_tensor).float()
        label_tensor = Variable(label_tensor).long()
        if self.gpu > -1:
            input_tensor = input_tensor.to(self.gpu)
            label_tensor = label_tensor.to(self.gpu)

        return input_tensor, label_tensor

    def train_forward_backward(self, input_tensor, label_tensor):
        # Zero the gradient
        self.optimizer.zero_grad()

        # Get model predictions, calculate loss, backprop
        prediction_tensor = self.model(input_tensor)
        loss = self.criterion(prediction_tensor, label_tensor)
        loss.backward()
        self.optimizer.step()
        return prediction_tensor, loss

    def eval_forward(self, input_tensor, label_tensor):
        # Get predictions and calculate loss
        prediction_tensor = self.model(input_tensor)
        loss = self.criterion(prediction_tensor, label_tensor)
        return prediction_tensor, loss

    def train_model(self):
        self.model.train()

        for input_tensor, label_tensor in self.train_loader:
            input_tensor, label_tensor = self.tensorize_batch(
                input_tensor, label_tensor)

            prediction_tensor, loss = self.train_forward_backward(
                input_tensor, label_tensor)
            self.train_metrics.compute(prediction_tensor, label_tensor, loss)

            # clear batch variables from memory
            del input_tensor, label_tensor

        return self.train_metrics.crunch_it(self.epoch)

    def eval_model(self):
        self.model.eval()

        for input_tensor, label_tensor in self.train_loader:
            input_tensor, label_tensor = self.tensorize_batch(
                input_tensor, label_tensor)

            prediction_tensor, loss = self.eval_forward(
                input_tensor, label_tensor)
            self.val_metrics.compute(prediction_tensor, label_tensor, loss)

            # clear batch variables from memory
            del input_tensor, label_tensor

        return self.val_metrics.crunch_it(self.epoch)
