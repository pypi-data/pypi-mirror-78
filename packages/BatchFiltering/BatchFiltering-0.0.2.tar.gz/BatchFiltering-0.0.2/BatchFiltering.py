import torch
import torch.nn.functional as F


def _compute_squared_euclidean_distances(input):
    """
    Compute the squared Euclidean distances between the row vectors of the input.

    Args:
        input: The input tensor must have the shape of (N,C).
    Return:
        The NxN squared Euclidean distance matrix.
    """

    n = input.size(0)
    return torch.pow(input.unsqueeze(1).expand(-1, n, -1) - input.unsqueeze(0).expand(n, -1, -1), 2).sum(2)


def _compute_graph_laplacian(squared_dists, sigma=1.0):
    """
    Compute the Laplacian of the graph describe as a matrix of pairwise distances.

    Args:
         squared_dists: The NxN squared pairwise distance matrix.
         sigma: The scale of Gaussian kernel for computing affinity from distance.
    Return:
        The NxN graph Laplacian matrix.
    """

    affinities = torch.exp(-squared_dists / (2 * sigma * sigma)).fill_diagonal_(0.0)
    return torch.diag(torch.sum(affinities, dim=1)) - affinities


class _BatchFiltering1D(torch.autograd.Function):
    """
    The 1D batch filtering operator applies low-pass filtering to the gradients
    received by a mini-batch of 1D feature vectors in a neural network architecture.
    The gradients can originate from minimizing some classification loss, regression loss,
    or adversarial losses.
    """

    @staticmethod
    def forward(ctx, input, gamma=0.0, sigma=1.0):
        """
        The forward pass returns the input as it is.

        Args:
            ctx: The context object.
            input: The input tensor must have the shape of (N,C).
            gamma: The strength of batch filtering (default=0.0).
            sigma: The scale of Gaussian kernel for affinity computation (default=1.0).

        Return:
            The input tensor.
        """

        if input.dim() != 2 or input.size(0) <= 1:
            raise ValueError('The input tensor must have the shape of (N,C) and N must be greater than 1')

        if gamma < 0:
            raise ValueError('The gamma parameter must not be smaller than 0')

        if sigma <= 0:
            raise ValueError('The sigma parameter must be greater than 0')

        ctx.input = input
        ctx.gamma = gamma
        ctx.sigma = sigma
        return input

    @staticmethod
    def backward(ctx, grad_output):
        """
        The backward pass filters the gradients based on the affinity of the input samples.

        Args:
            ctx: The context object.
            grad_output: The original gradients.

        Return:
            The filtered gradients with respect to the input tensor, and none for the other arguments.
        """

        input, gamma, sigma = ctx.input, ctx.gamma, ctx.sigma

        with torch.no_grad():
            # Normalize the features
            input = F.normalize(input, p=2, dim=1)

            # Compute the Laplacian
            laplacian = _compute_graph_laplacian(_compute_squared_euclidean_distances(input), sigma)

            # Solve for the filtered gradients
            grad_filter = torch.inverse(torch.eye(input.size(0)) + min(gamma, 1e3) * torch.matmul(laplacian, laplacian))
            grad_output_filtered = torch.matmul(grad_filter, grad_output)

        return grad_output_filtered, None, None


class _BatchFiltering2D(torch.autograd.Function):
    """
    The 2D batch filtering operator applies low-pass filtering to the gradients
    received by a mini-batch of 2D feature maps or images in a neural network
    architecture. The gradients can originate from minimizing some classification loss,
    regression loss, or adversarial losses.
    """

    @staticmethod
    def forward(ctx, input, gamma=0.0, sigma=1.0):
        """
        The forward pass returns the input as it is.

        Args:
            ctx: The context object.
            input: The input tensor must have the shape of (N,C,H,W).
            gamma: The strength of batch filtering (default=0.0).
            sigma: The scale of Gaussian kernel for affinity computation (default=1.0).

        Return:
            The input tensor.
        """

        if input.dim() != 4 or input.size(0) <= 1:
            raise ValueError('The input tensor must have the shape of (N,C,H,W) and N must be greater than 1')

        if gamma < 0:
            raise ValueError('The gamma parameter must not be smaller than 0')

        if sigma <= 0:
            raise ValueError('The sigma parameter must be greater than 0')

        ctx.input = input
        ctx.gamma = gamma
        ctx.sigma = sigma
        return input

    @staticmethod
    def backward(ctx, grad_output):
        """
        The backward pass filters the gradients based on the affinity of the input samples.

        Args:
            ctx: The context object.
            grad_output: The original gradients.

        Return:
            The filtered gradients with respect to the input tensor, and none for the other arguments.
        """

        input, gamma, sigma = ctx.input, ctx.gamma, ctx.sigma

        with torch.no_grad():
            # Perform global average pooling
            input = torch.mean(input, dim=(2, 3))

            # Normalize the features
            input = F.normalize(input, p=2, dim=1)

            # Compute the Laplacian
            laplacian = _compute_graph_laplacian(_compute_squared_euclidean_distances(input), sigma)

            # Solve for the filtered gradients
            grad_filter = torch.inverse(torch.eye(input.size(0)) + min(gamma, 1e3) * torch.matmul(laplacian, laplacian))
            grad_output_filtered = torch.reshape(torch.matmul(grad_filter, torch.flatten(grad_output, start_dim=1)),
                                                 grad_output.size())

        return grad_output_filtered, None, None


# Public functions that can be just called like a standard activation function
batch_filtering1d = _BatchFiltering1D.apply
batch_filtering2d = _BatchFiltering2D.apply
