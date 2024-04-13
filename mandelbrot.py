import numpy as np
import matplotlib.pyplot as plt


def mandelbrot(c, max_iter):
    z = 0
    n = 0
    while abs(z) <= 2 and n < max_iter:
        z = z * z + c
        n += 1
    if n == max_iter:
        return max_iter
    return n + 1 - np.log(np.log2(abs(z)))


width, height = 800, 800
max_iter = 256

real = np.linspace(-2.0, 1.0, width)
imag = np.linspace(-1.5, 1.5, height)
real_grid, imag_grid = np.meshgrid(real, imag)
c = real_grid + imag_grid * 1j
output = np.vectorize(mandelbrot)(c, max_iter)

plt.figure(figsize=(10, 10))
plt.imshow(output.T, cmap="hot", interpolation="bilinear", extent=[-2, 1, -1.5, 1.5])
plt.colorbar()
plt.title("Fractal de Mandelbrot para DSI (Design Systems inno)")
plt.axis("off")
plt.show()
