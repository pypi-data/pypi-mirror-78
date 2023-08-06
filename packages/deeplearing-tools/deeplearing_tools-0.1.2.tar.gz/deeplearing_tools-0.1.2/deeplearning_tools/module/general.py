from torch import nn

__all__ = ['CBAModule', 'UpSampleModule']


# Conv BatchNorm Activation
class CBAModule(nn.Module):
    def __init__(self, in_channels, out_channels=24, kernel_size=3, stride=1, padding=0, bias=False):
        super(CBAModule, self).__init__()
        self.conv = nn.Conv2d(in_channels, out_channels, kernel_size, stride, padding=padding, bias=bias)
        self.bn = nn.BatchNorm2d(out_channels)
        self.act = nn.ReLU(inplace=True)

    def forward(self, x):
        x = self.conv(x)
        x = self.bn(x)
        x = self.act(x)
        return x


# Up Sample Module
class UpSampleModule(nn.Module):
    """
    上采样
    """
    def __init__(self, in_channels, out_channels, kernel_size=2, stride=2, bias=False, mode="UCBA"):
        super(UpSampleModule, self).__init__()
        self.mode = mode

        if self.mode == "UCBA":
            self.up = nn.UpsamplingBilinear2d(scale_factor=2)
            self.conv = CBAModule(in_channels, out_channels, 3, padding=1, bias=bias)
        elif self.mode == "DeconvBN":
            self.dconv = nn.ConvTranspose2d(in_channels, out_channels, kernel_size, stride, bias=bias)
            self.bn = nn.BatchNorm2d(out_channels)
            self.relu = nn.ReLU()
        elif self.mode == "DeCBA":
            self.dconv = nn.ConvTranspose2d(in_channels, out_channels, kernel_size, stride, bias=bias)
            self.conv = CBAModule(out_channels, out_channels, 3, padding=1, bias=bias)
        else:
            raise RuntimeError(f"Unsupport mode: {mode}")

    def forward(self, x):
        if self.mode == "UCBA":
            return self.conv(self.up(x))
        elif self.mode == "DeconvBN":
            return self.relu(self.bn(self.dconv(x)))
        elif self.mode == "DeCBA":
            return self.conv(self.dconv(x))
