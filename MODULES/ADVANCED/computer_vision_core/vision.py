"""
MODULE #30: COMPUTER VISION CORE
Instance 3: Module Developer
Built: 2025-11-08

Image processing, edge detection, pattern recognition, basic CV operations.
"""

import numpy as np
from typing import List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class BoundingBox:
    """Bounding box for detected object"""
    x: int
    y: int
    width: int
    height: int
    confidence: float


class ImageProcessor:
    """
    Computer Vision toolkit for image processing

    Features:
    - Edge detection
    - Filters (blur, sharpen)
    - Feature detection
    - Object detection (basic)
    - Image transformations
    """

    @staticmethod
    def convolve2d(image: np.ndarray, kernel: np.ndarray) -> np.ndarray:
        """Apply 2D convolution"""

        img_h, img_w = image.shape
        ker_h, ker_w = kernel.shape

        # Output size
        out_h = img_h - ker_h + 1
        out_w = img_w - ker_w + 1

        output = np.zeros((out_h, out_w))

        for i in range(out_h):
            for j in range(out_w):
                region = image[i:i+ker_h, j:j+ker_w]
                output[i, j] = np.sum(region * kernel)

        return output

    @staticmethod
    def gaussian_blur(image: np.ndarray, kernel_size: int = 5) -> np.ndarray:
        """Apply Gaussian blur"""

        # Create Gaussian kernel
        sigma = kernel_size / 6
        ax = np.arange(-kernel_size // 2 + 1, kernel_size // 2 + 1)
        xx, yy = np.meshgrid(ax, ax)

        kernel = np.exp(-(xx**2 + yy**2) / (2 * sigma**2))
        kernel = kernel / np.sum(kernel)

        # Apply convolution
        return ImageProcessor.convolve2d(image, kernel)

    @staticmethod
    def sobel_edge_detection(image: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Sobel edge detection

        Returns:
            (magnitude, direction)
        """

        # Sobel kernels
        sobel_x = np.array([[-1, 0, 1],
                           [-2, 0, 2],
                           [-1, 0, 1]])

        sobel_y = np.array([[-1, -2, -1],
                           [0, 0, 0],
                           [1, 2, 1]])

        # Apply filters
        grad_x = ImageProcessor.convolve2d(image, sobel_x)
        grad_y = ImageProcessor.convolve2d(image, sobel_y)

        # Calculate magnitude and direction
        magnitude = np.sqrt(grad_x**2 + grad_y**2)
        direction = np.arctan2(grad_y, grad_x)

        return magnitude, direction

    @staticmethod
    def harris_corner_detection(image: np.ndarray, threshold: float = 0.01) -> List[Tuple[int, int]]:
        """Harris corner detection"""

        # Compute gradients
        sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
        sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])

        Ix = ImageProcessor.convolve2d(image, sobel_x)
        Iy = ImageProcessor.convolve2d(image, sobel_y)

        # Products of derivatives
        Ixx = Ix ** 2
        Iyy = Iy ** 2
        Ixy = Ix * Iy

        # Sum over window (simplified - no window function)
        k = 0.04

        # Harris response
        det = Ixx * Iyy - Ixy ** 2
        trace = Ixx + Iyy
        R = det - k * trace ** 2

        # Threshold
        corners = []
        threshold_value = threshold * np.max(R)

        for i in range(R.shape[0]):
            for j in range(R.shape[1]):
                if R[i, j] > threshold_value:
                    corners.append((i, j))

        return corners

    @staticmethod
    def resize(image: np.ndarray, new_height: int, new_width: int) -> np.ndarray:
        """Resize image using nearest neighbor"""

        old_h, old_w = image.shape
        resized = np.zeros((new_height, new_width))

        h_ratio = old_h / new_height
        w_ratio = old_w / new_width

        for i in range(new_height):
            for j in range(new_width):
                old_i = int(i * h_ratio)
                old_j = int(j * w_ratio)
                resized[i, j] = image[old_i, old_j]

        return resized

    @staticmethod
    def threshold(image: np.ndarray, threshold: float) -> np.ndarray:
        """Binary thresholding"""
        return (image > threshold).astype(np.uint8) * 255

    @staticmethod
    def normalize(image: np.ndarray) -> np.ndarray:
        """Normalize image to 0-255"""
        min_val = np.min(image)
        max_val = np.max(image)

        if max_val == min_val:
            return np.zeros_like(image)

        normalized = (image - min_val) / (max_val - min_val) * 255

        return normalized.astype(np.uint8)


def demo():
    """Demonstrate computer vision capabilities"""

    print("=" * 60)
    print("COMPUTER VISION DEMO")
    print("=" * 60)
    print()

    # Create synthetic image
    image = np.random.rand(50, 50) * 255

    # Add some structure (rectangle)
    image[15:35, 15:35] = 200

    print(f"Created synthetic image: {image.shape}")
    print()

    # Edge detection
    print("EDGE DETECTION:")
    magnitude, direction = ImageProcessor.sobel_edge_detection(image)
    print(f"  Edge magnitude range: {np.min(magnitude):.2f} to {np.max(magnitude):.2f}")
    print()

    # Corner detection
    print("CORNER DETECTION:")
    corners = ImageProcessor.harris_corner_detection(image, threshold=0.01)
    print(f"  Detected {len(corners)} corners")
    if corners:
        print(f"  First 3 corners: {corners[:3]}")
    print()

    # Gaussian blur
    print("GAUSSIAN BLUR:")
    blurred = ImageProcessor.gaussian_blur(image, kernel_size=5)
    print(f"  Blurred image shape: {blurred.shape}")
    print()

    # Resize
    print("RESIZE:")
    resized = ImageProcessor.resize(image, 25, 25)
    print(f"  Original: {image.shape}, Resized: {resized.shape}")
    print()

    # Threshold
    print("THRESHOLDING:")
    binary = ImageProcessor.threshold(image, threshold=150)
    print(f"  Binary image: {np.sum(binary == 255)} white pixels")
    print()

    print("=" * 60)
    print("COMPUTER VISION DEMO COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    demo()
