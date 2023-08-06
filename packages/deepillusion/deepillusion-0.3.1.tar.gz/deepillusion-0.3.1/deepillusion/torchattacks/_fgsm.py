"""
Description: Fast Gradient Sign Method
Goodfellow [https://arxiv.org/abs/1412.6572]

Example Use:

fgsm_args = dict(net=net,
                 x=x,
                 y_true=y_true,
                 data_params={"x_min": 0.,
                              "x_max": 1.},
                 attack_params={"norm": "inf",
                                "eps": 8.0/255})
perturbs = FGSM(**fgsm_args)
data_adversarial = data + perturbs

fgsm_targeted_args = dict(net=net,
                          x=x,
                          y_target=y_target,
                          data_params={"x_min": 0.,
                                       "x_max": 1.},
                          attack_params={"norm": "inf",
                                         "eps": 8.0/255})
perturbs = FGSM_targeted(**fgsm_targeted_args)
data_adversarial = data + perturbs

"""

import torch
from torch import nn
from warnings import warn

from .._utils import GradientMaskingWarning, GradientMaskingError
from ._utils import clip, to_one_hot

__all__ = ["FGSM", "FGSM_targeted", "FGM"]


def FGSM(net, x, y_true, data_params, attack_params, loss_function="cross_entropy", verbose=False):
    """
    Description: Fast gradient sign method
        Goodfellow [https://arxiv.org/abs/1412.6572]
    Input :
        net : Neural Network                                        (torch.nn.Module)
        x : Inputs to the net                                       (Batch)
        y_true : Labels                                             (Batch)
        data_params :                                               (dict)
            x_min:  Minimum possible value of x (min pixel value)   (Float)
            x_max:  Maximum possible value of x (max pixel value)   (Float)
        attack_params : Attack parameters as a dictionary           (dict)
            norm : Norm of attack                                   (Str)
            eps : Attack budget                                     (Float)
        verbose: Check for gradient masking                         (Bool)
    Output:
        perturbation : Single step perturbation (Clamped with input limits)

    Explanation:
        e = epsilon * sign(grad_{x}(net(x)))
    """
    e = torch.zeros_like(x, requires_grad=True)  # perturbation

    # Increase precision to prevent gradient masking
    if x.device.type == "cuda":
        y_hat = net(x + e).type(torch.cuda.DoubleTensor)
    else:
        y_hat = net(x + e)

    # Overcome batch_size=1 error issue
    y_hat = y_hat.view(-1, y_hat.shape[-1])

    # Loss computation
    if loss_function == "cross_entropy":
        criterion = nn.CrossEntropyLoss(reduction="none")
        loss = criterion(y_hat, y_true)
    elif loss_function == "carlini_wagner":
        num_classes = y_hat.shape[-1]
        y_true_onehot = to_one_hot(y_true, num_classes).to(x.device)

        correct_logit = (y_true_onehot * y_hat).sum(dim=1)
        wrong_logit = ((1 - y_true_onehot) * y_hat - 1e4 * y_true_onehot).max(dim=1)[0]

        loss = -nn.functional.relu(correct_logit - wrong_logit + 50)
    else:
        raise NotImplementedError

    # Calculating backprop for images
    loss.backward(gradient=torch.ones_like(y_true, dtype=torch.float), retain_graph=True)
    e_grad = e.grad.data

    if verbose:
        # To make sure Gradient Masking is not happening
        max_attack_for_each_image, _ = e_grad.abs().view(e.size(0), -1).max(dim=1)
        if max_attack_for_each_image.min() <= 0:
            warn("Gradient Masking is happening for some images!!!!!", GradientMaskingWarning)

    if attack_params["norm"] == "inf":
        perturbation = attack_params["eps"] * e_grad.sign()
    else:
        perturbation = e_grad * attack_params["eps"] / \
            e_grad.view(e.shape[0], -1).norm(p=attack_params["norm"], dim=-1).view(-1, 1, 1, 1)

    # Clipping perturbations so that  x_min < image + perturbation < x_max
    perturbation.data = clip(perturbation, data_params["x_min"] - x, data_params["x_max"] - x)
    return perturbation


def FGM(net, x, y_true, loss_function="cross_entropy",  verbose=False):
    """
    Description: Fast gradient method (without sign gives gradients as it is)
        Goodfellow [https://arxiv.org/abs/1412.6572]
    Input :
        net : Neural Network                                        (torch.nn.Module)
        x : Inputs to the net                                       (Batch)
        y_true : Labels                                             (Batch)
        data_params :                                               (dict)
            x_min:  Minimum possible value of x (min pixel value)   (Float)
            x_max:  Maximum possible value of x (max pixel value)   (Float)
        attack_params : Attack parameters as a dictionary           (dict)
        verbose: Check for gradient masking                         (Bool)
    Output:
        perturbation : Single step perturbation (Clamped with input limits)

    Explanation:
        e = epsilon * sign(grad_{x}(net(x)))
    """
    e = torch.zeros_like(x, requires_grad=True)  # perturbation

    # Increase precision to prevent gradient masking
    if x.device.type == "cuda":
        y_hat = net(x + e).type(torch.cuda.DoubleTensor)
    else:
        y_hat = net(x + e)

    # Overcome batch_size=1 error issue
    y_hat = y_hat.view(-1, y_hat.shape[-1])

    # Loss computation
    if loss_function == "cross_entropy":
        criterion = nn.CrossEntropyLoss(reduction="none")
        loss = criterion(y_hat, y_true)
    elif loss_function == "carlini_wagner":
        num_classes = y_hat.shape[-1]
        y_true_onehot = to_one_hot(y_true, num_classes).to(x.device)

        correct_logit = (y_true_onehot * y_hat).sum(dim=1)
        wrong_logit = ((1 - y_true_onehot) * y_hat - 1e4 * y_true_onehot).max(dim=1)[0]

        loss = -nn.functional.relu(correct_logit - wrong_logit + 50)
    else:
        raise NotImplementedError

    # Calculating backprop for images
    loss.backward(gradient=torch.ones_like(y_true, dtype=torch.float), retain_graph=True)
    e_grad = e.grad.data

    if verbose:
        # To make sure Gradient Masking is not happening
        max_attack_for_each_image, _ = e_grad.abs().view(e.size(0), -1).max(dim=1)
        if max_attack_for_each_image.min() <= 0:
            warn("Gradient Masking is happening for some images!!!!!", GradientMaskingWarning)

    perturbation = e_grad

    return perturbation


def FGSM_targeted(net, x, y_true, y_target, data_params, attack_params, loss_function="cross_entropy", verbose=False):
    """
    Description: Fast gradient sign method
        Goodfellow [https://arxiv.org/abs/1412.6572]
    Input :
        net : Neural Network                                        (torch.nn.Module)
        x : Inputs to the net                                       (Batch)
        y_target : Target label                                     (Batch)
        data_params :                                               (dict)
            x_min:  Minimum possible value of x (min pixel value)   (Float)
            x_max:  Maximum possible value of x (max pixel value)   (Float)
        attack_params : Attack parameters as a dictionary           (dict)
            norm : Norm of attack                                   (Str)
            eps : Attack budget                                     (Float)
        verbose: Check for gradient masking                         (Bool)
    Output:
        perturbation : Single step perturbation (Clamped with input limits)

    Explanation:
        e = epsilon * sign(grad_{x}(net(x)))
    """
    e = torch.zeros_like(x, requires_grad=True)  # perturbation

    # Increase precision to prevent gradient masking
    if x.device.type == "cuda":
        y_hat = net(x + e).type(torch.cuda.DoubleTensor)
    else:
        y_hat = net(x + e)

    # Overcome batch_size=1 error issue
    y_hat = y_hat.view(-1, y_hat.shape[-1])

    # Loss computation
    if loss_function == "cross_entropy":
        criterion = nn.CrossEntropyLoss(reduction="none")
        loss = criterion(y_hat, y_target)
    elif loss_function == "carlini_wagner":
        num_classes = y_hat.shape[-1]
        y_true_onehot = to_one_hot(y_true, num_classes).to(x.device)

        correct_logit = (y_true_onehot * y_hat).sum(dim=1)
        target_logit = y_hat[:, y_target]

        loss = -nn.functional.relu(correct_logit - target_logit + 50)
    else:
        raise NotImplementedError

    # Calculating backprop for images
    loss.backward(gradient=torch.ones_like(y_target, dtype=torch.float), retain_graph=True)
    e_grad = e.grad.data

    if verbose:
        # To make sure Gradient Masking is not happening
        max_attack_for_each_image, _ = e_grad.abs().view(e.size(0), -1).max(dim=1)
        if max_attack_for_each_image.min() <= 0:
            warn("Gradient Masking is happening for some images!!!!!", GradientMaskingWarning)

    if attack_params["norm"] == "inf":
        perturbation = -attack_params["eps"] * e_grad.sign()
    else:
        perturbation = -e_grad * attack_params["eps"] / \
            e_grad.view(e.shape[0], -1).norm(p=attack_params["norm"], dim=-1).view(-1, 1, 1, 1)

    # Clipping perturbations so that  x_min < image + perturbation < x_max
    perturbation.data = clip(perturbation, data_params["x_min"] - x, data_params["x_max"] - x)

    return perturbation
