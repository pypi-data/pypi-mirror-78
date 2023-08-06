"""
Description: Basic Iterative Method

Example Use:

bim_args = dict(net=model,
                x=x,
                y_true=y_true,
                data_params={"x_min": 0.,
                             "x_max": 1.},
                attack_params={"norm": "inf",
                               "eps": 8./255,
                               "step_size": 2./255,
                               "num_steps": 7},
                verbose=False,
                progress_bar=False)
perturbation = BIM(**bim_args)
data_adversarial = data + perturbation
"""

from tqdm import tqdm
import torch

from ._fgsm import FGSM, FGM
from ._utils import clip

__all__ = ["BIM", "BIM_EOT"]


def BIM(net, x, y_true, data_params, attack_params, loss_function="cross_entropy", verbose=False, progress_bar=False):
    """
    Description: Basic Iterative Method
    Input :
        net : Neural Network                                        (torch.nn.Module)
        x : Inputs to the net                                       (Batch)
        y_true : Labels                                             (Batch)
        data_params :                                               (dict)
            x_min:  Minimum possible value of x (min pixel value)   (Float)
            x_max:  Maximum possible value of x (max pixel value)   (Float)
        attack_params : Attack parameters as a dictionary           (dict)
                norm : Norm of attack                               (Str)
                eps : Attack budget                                 (Float)
                step_size : Attack budget for each iteration        (Float)
                num_steps : Number of iterations                    (Int)
        verbose: check gradient masking                             (Bool)
        progress_bar: Put progress bar                              (Bool)
    Output:
        perturbation : Perturbations for given batch                (Batch)

    Explanation:
        e = zeros()
        repeat num_steps:
            e += delta * sign(grad_{x}(loss(net(x))))
    """

    # setting parameters.requires_grad = False increases speed
    requires_grad_save = [True]*len(list(net.parameters()))
    for i, p in enumerate(net.parameters()):
        requires_grad_save[i] = p.requires_grad
        p.requires_grad = False

    perturbation = torch.zeros_like(x, dtype=torch.float)

    # Adding progress bar for iterations if progress_bar = True
    if progress_bar:
        iters = tqdm(
            iterable=range(attack_params["num_steps"]),
            desc="Attack Steps Progress",
            unit="step",
            leave=False)
    else:
        iters = range(attack_params["num_steps"])

    for _ in iters:
        fgsm_args = dict(net=net,
                         x=x+perturbation,
                         y_true=y_true,
                         data_params=data_params,
                         attack_params={"norm": attack_params["norm"],
                                        "eps": attack_params["step_size"]},
                         loss_function=loss_function,
                         verbose=verbose)
        perturbation += FGSM(**fgsm_args)

        # Clip perturbation if surpassed the norm bounds
        if attack_params["norm"] == "inf":
            perturbation = torch.clamp(
                perturbation, -attack_params["eps"], attack_params["eps"])
        else:
            perturbation = (perturbation * attack_params["eps"] /
                            perturbation.view(x.shape[0], -1).norm(p=attack_params["norm"], dim=-1).view(-1, 1, 1, 1))

    # set back to saved values
    for i, p in enumerate(net.parameters()):
        p.requires_grad = requires_grad_save[i]

    return perturbation


def BIM_EOT(net, x, y_true, data_params, attack_params, loss_function="cross_entropy", verbose=False, progress_bar=False):
    """
    Description: Basic Iterative Method
    Input :
        net : Neural Network                                        (torch.nn.Module)
        x : Inputs to the net                                       (Batch)
        y_true : Labels                                             (Batch)
        data_params :                                               (dict)
            x_min:  Minimum possible value of x (min pixel value)   (Float)
            x_max:  Maximum possible value of x (max pixel value)   (Float)
        attack_params : Attack parameters as a dictionary           (dict)
                norm : Norm of attack                               (Str)
                eps : Attack budget                                 (Float)
                step_size : Attack budget for each iteration        (Float)
                num_steps : Number of iterations                    (Int)
        verbose: check gradient masking                             (Bool)
        progress_bar: Put progress bar                              (Bool)
    Output:
        perturbation : Perturbations for given batch                (Batch)

    Explanation:
        e = zeros()
        repeat num_steps:
            e += delta * sign(grad_{x}(loss(net(x))))
    """

    # setting parameters.requires_grad = False increases speed
    requires_grad_save = [True]*len(list(net.parameters()))
    for i, p in enumerate(net.parameters()):
        requires_grad_save[i] = p.requires_grad
        p.requires_grad = False

    perturbation = torch.zeros_like(x, dtype=torch.float)

    # Adding progress bar for iterations if progress_bar = True
    if progress_bar:
        iters = tqdm(
            iterable=range(attack_params["num_steps"]),
            desc="Attack Steps Progress",
            unit="step",
            leave=False)
    else:
        iters = range(attack_params["num_steps"])

    for _ in iters:
        fgm_args = dict(net=net,
                        x=torch.clamp(x+perturbation,
                                      data_params["x_min"], data_params["x_max"]),
                        y_true=y_true,
                        loss_function=loss_function,
                        verbose=verbose)
        # Adding progress bar for ensemble if progress_bar = True
        if progress_bar:
            ensemble = tqdm(
                iterable=range(attack_params["EOT_size"]),
                desc="EOT Runs Progress",
                unit="element",
                leave=False)
        else:
            ensemble = range(attack_params["EOT_size"])

        expected_grad = 0
        for _ in ensemble:
            e_grad = FGM(**fgm_args)
            expected_grad += e_grad

        # Clip perturbation if surpassed the norm bounds
        if attack_params["norm"] == "inf":
            perturbation += attack_params["step_size"] * expected_grad.sign()
            perturbation = torch.clamp(
                perturbation, -attack_params["eps"], attack_params["eps"])
        else:
            perturbation += (expected_grad * attack_params["step_size"] /
                             expected_grad.view(x.shape[0], -1).norm(p=attack_params["norm"], dim=-1).view(-1, 1, 1, 1))
            perturbation = (perturbation * attack_params["eps"] /
                            perturbation.view(x.shape[0], -1).norm(p=attack_params["norm"], dim=-1).view(-1, 1, 1, 1))

        perturbation = clip(
            perturbation, data_params["x_min"] - x, data_params["x_max"] - x)

    # set back to saved values
    for i, p in enumerate(net.parameters()):
        p.requires_grad = requires_grad_save[i]

    return perturbation
