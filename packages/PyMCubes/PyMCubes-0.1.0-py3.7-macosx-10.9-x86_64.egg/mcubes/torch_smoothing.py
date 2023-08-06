
import numpy as np
from scipy import ndimage as ndi
import torch
from torch.nn.functional import pad

__all__ = ['torch_smooth']

FILTER2D = torch.tensor([
    [[[0, 0, 0],
      [1, -2, 1],
      [0, 0, 0]]],
    [[[0, -1, 0],
      [0, 2, 0],
      [0, -1, 0]]]
], dtype=torch.float32)

FILTER3D = torch.tensor([
    [[
        [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 0]],
        [[0, 0, 0],
         [1, -2, 1],
         [0, 0, 0]],
        [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 0]]
    ]],
    [[
        [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 0]],
        [[0, 1, 0],
         [0, -2, 0],
         [0, 1, 0]],
        [[0, 0, 0],
         [0, 0, 0],
         [0, 0, 0]]
    ]],
    [[
        [[0, 0, 0],
         [0, 1, 0],
         [0, 0, 0]],
        [[0, 0, 0],
         [0, -2, 0],
         [0, 0, 0]],
        [[0, 0, 0],
         [0, 1, 0],
         [0, 0, 0]]
    ]]
], dtype=torch.float32)

DIFFFILTER_2D = torch.tensor([
    [[[0, 0, 1, 0, 0],
      [0, 0, -4, 0, 0],
      [1, -4, 12, -4, 1],
      [0, 0, -4, 0, 0],
      [0, 0, 1, 0, 0]]],
], dtype=torch.float32)

JACOBI_R_2D = torch.tensor([
    [[[0, 0, 1, 0, 0],
      [0, 0, -4, 0, 0],
      [1, -4, 0, -4, 1],
      [0, 0, -4, 0, 0],
      [0, 0, 1, 0, 0]]],
], dtype=torch.float32)
JACOBI_D_2D = 1/12

DIFFFILTER_3D = torch.tensor([[
    [
    [[0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0],
     [0, 0, 1, 0, 0],
     [0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0]],
    [[0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0],
     [0, 0, -4, 0, 0],
     [0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0]],
    [[0, 0, 1, 0, 0],
     [0, 0, -4, 0, 0],
     [1, -4, 18, -4, 1],
     [0, 0, -4, 0, 0],
     [0, 0, 1, 0, 0]],
    [[0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0],
     [0, 0, -4, 0, 0],
     [0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0]],
    [[0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0],
     [0, 0, 1, 0, 0],
     [0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0]]
    ]
]], dtype=torch.float32)

JACOBI_R_3D = torch.tensor([[
    [
    [[0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0],
     [0, 0, 1, 0, 0],
     [0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0]],
    [[0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0],
     [0, 0, -4, 0, 0],
     [0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0]],
    [[0, 0, 1, 0, 0],
     [0, 0, -4, 0, 0],
     [1, -4, 0, -4, 1],
     [0, 0, -4, 0, 0],
     [0, 0, 1, 0, 0]],
    [[0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0],
     [0, 0, -4, 0, 0],
     [0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0]],
    [[0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0],
     [0, 0, 1, 0, 0],
     [0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0]]
    ]
]], dtype=torch.float32)

JACOBI_D_3D = 1/18

assert FILTER2D.shape == (2, 1, 3, 3)
assert FILTER3D.shape == (3, 1, 3, 3, 3)


def signed_distance_function(binary_arr: np.ndarray) -> np.ndarray:

    arr = np.where(binary_arr > 0, 1.0, 0.0)
    dist_func = ndi.distance_transform_edt
    distance = np.where(
        binary_arr,
        dist_func(arr) - 0.5,
        -dist_func(1 - arr) + 0.5
    )
    return distance


def energy(arr: torch.Tensor) -> torch.Tensor:

    arr = arr[None, None]

    if arr.dim() == 4:
        pad_array = pad(arr, [1, 1, 1, 1], mode='replicate')
        diff2 = torch.conv2d(pad_array, FILTER2D)[0]
    elif arr.dim() == 5:
        pad_array = pad(arr, [1, 1, 1, 1, 1, 1], mode='replicate')
        diff2 = torch.conv3d(pad_array, FILTER3D)[0]
    else:
        raise ValueError('arr.dim() must be 2 or 3')

    return torch.sum(diff2**2) / 2


def solve(
        arr: np.ndarray,
        lower_bound: np.ndarray,
        upper_bound: np.ndarray,
        max_iters: int = 100000,
        tol=1e-3
        ) -> np.ndarray:

    arr = torch.tensor(arr, requires_grad=True, dtype=torch.float32)
    lower_bound = torch.tensor(lower_bound, dtype=torch.float32)
    upper_bound = torch.tensor(upper_bound, dtype=torch.float32)

    optimizer = torch.optim.SGD([arr], lr=1e-2, momentum=0)

    energy_it = energy(arr)
    for it in range(max_iters):

        optimizer.zero_grad()
        energy_it.backward()
        optimizer.step()

        if (it + 1) % 1 == 0:
            print(energy_it)

        with torch.no_grad():
            lower_mask = arr < lower_bound
            arr[lower_mask] = lower_bound[lower_mask]
            upper_mask = arr > upper_bound
            arr[upper_mask] = upper_bound[upper_mask]

        energy_itm1 = energy_it
        energy_it = energy(arr)

        if energy_itm1 - energy_it < tol:
            break

    return arr.detach().cpu().numpy()


def diff_energy(arr: torch.Tensor) -> torch.Tensor:

    arr = arr[None, None]
    pad_array = arr

    if arr.dim() == 4:
        # pad_array = pad(arr, [2, 2, 2, 2], mode='replicate')
        return torch.conv2d(pad_array, DIFFFILTER_2D)[0, 0]

    if arr.dim() == 5:
        pad_array = pad(arr, [2, 2, 2, 2, 2, 2], mode='replicate')
        return torch.conv3d(pad_array, DIFFFILTER_3D)[0, 0]

    raise ValueError('arr.dim() must be 2 or 3')


def jacobi_r(arr: torch.Tensor) -> torch.Tensor:

    arr = arr[None, None]
    pad_array = arr

    if arr.dim() == 4:
        # pad_array = pad(arr, [2, 2, 2, 2], mode='replicate')
        return torch.conv2d(pad_array, JACOBI_R_2D)[0, 0]

    if arr.dim() == 5:
        pad_array = pad(arr, [2, 2, 2, 2, 2, 2], mode='replicate')
        return torch.conv3d(pad_array, JACOBI_R_3D)[0, 0]

    raise ValueError('arr.dim() must be 2 or 3')


@torch.no_grad()
def solve_jacobi(
        arr: np.ndarray,
        lower_bound: np.ndarray,
        upper_bound: np.ndarray,
        max_iters: int = 100000,
        jacobi_weight: float = 0.5
        ) -> np.ndarray:

    arr = torch.tensor(arr, dtype=torch.float32)
    lower_bound = torch.tensor(lower_bound, dtype=torch.float32)
    upper_bound = torch.tensor(upper_bound, dtype=torch.float32)

    jacobi_d = JACOBI_D_2D if arr.dim() == 2 else JACOBI_D_3D

    for it in range(max_iters):
        # energy_it = torch.sum(diff_energy(arr) * arr[2:-2, 2:-2, 2:-2]) / 2
        # energy_it = torch.sum(diff_energy(arr) * arr) / 2
        energy_it = energy(arr)
        print("Energy in iteration {}: {:.4g}".format(it, energy_it))

        arr_1 = - jacobi_d * jacobi_r(arr)
        # arr[2:-2, 2:-2, 2:-2] = jacobi_weight * arr_1 + (1 - jacobi_weight) * arr[2:-2, 2:-2, 2:-2]
        arr = jacobi_weight * arr_1 + (1 - jacobi_weight) * arr

        arr = torch.max(arr, lower_bound)
        arr = torch.min(arr, upper_bound)


def torch_smooth(binary_array: np.ndarray, max_iters: int = 100000) -> np.ndarray:

    # binary_array = np.pad(binary_array, 2, mode='reflect')

    arr = signed_distance_function(binary_array)

    upper_bound = np.where(arr < 0, arr, np.inf)
    lower_bound = np.where(arr > 0, arr, -np.inf)

    return solve(arr, lower_bound, upper_bound, max_iters)
