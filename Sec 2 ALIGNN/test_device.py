import torch

def test_device():
    device = "cpu"
    if torch.cuda.is_available():
        device = torch.device("cuda")
    print(device)
    return device

test_device()