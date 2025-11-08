"""
MODULE #26: NEURAL NETWORK TRAINER
Instance 3: Module Developer
Built: 2025-11-08

Build and train neural networks from scratch.
No external ML libraries required - pure Python and NumPy.
"""

import numpy as np
import json
import time
from typing import List, Tuple, Dict, Any, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum


class ActivationFunction(Enum):
    """Activation functions for neural networks"""
    RELU = "relu"
    SIGMOID = "sigmoid"
    TANH = "tanh"
    SOFTMAX = "softmax"
    LINEAR = "linear"


class LossFunction(Enum):
    """Loss functions"""
    MSE = "mse"                    # Mean Squared Error
    BINARY_CROSSENTROPY = "bce"    # Binary Cross-Entropy
    CATEGORICAL_CROSSENTROPY = "cce"  # Categorical Cross-Entropy


@dataclass
class TrainingMetrics:
    """Track training progress"""
    epoch: int
    train_loss: float
    train_accuracy: float
    val_loss: Optional[float] = None
    val_accuracy: Optional[float] = None
    time_elapsed: float = 0.0


class Activation:
    """Activation functions and their derivatives"""

    @staticmethod
    def relu(x: np.ndarray) -> np.ndarray:
        """ReLU: max(0, x)"""
        return np.maximum(0, x)

    @staticmethod
    def relu_derivative(x: np.ndarray) -> np.ndarray:
        """Derivative of ReLU"""
        return (x > 0).astype(float)

    @staticmethod
    def sigmoid(x: np.ndarray) -> np.ndarray:
        """Sigmoid: 1 / (1 + e^(-x))"""
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))

    @staticmethod
    def sigmoid_derivative(x: np.ndarray) -> np.ndarray:
        """Derivative of sigmoid"""
        s = Activation.sigmoid(x)
        return s * (1 - s)

    @staticmethod
    def tanh(x: np.ndarray) -> np.ndarray:
        """Tanh: (e^x - e^(-x)) / (e^x + e^(-x))"""
        return np.tanh(x)

    @staticmethod
    def tanh_derivative(x: np.ndarray) -> np.ndarray:
        """Derivative of tanh"""
        return 1 - np.tanh(x) ** 2

    @staticmethod
    def softmax(x: np.ndarray) -> np.ndarray:
        """Softmax for multi-class classification"""
        exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
        return exp_x / np.sum(exp_x, axis=-1, keepdims=True)

    @staticmethod
    def linear(x: np.ndarray) -> np.ndarray:
        """Linear activation (identity)"""
        return x

    @staticmethod
    def linear_derivative(x: np.ndarray) -> np.ndarray:
        """Derivative of linear"""
        return np.ones_like(x)


class Layer:
    """Fully connected neural network layer"""

    def __init__(
        self,
        input_size: int,
        output_size: int,
        activation: ActivationFunction = ActivationFunction.RELU
    ):
        self.input_size = input_size
        self.output_size = output_size
        self.activation = activation

        # Xavier/Glorot initialization
        limit = np.sqrt(6 / (input_size + output_size))
        self.weights = np.random.uniform(-limit, limit, (input_size, output_size))
        self.biases = np.zeros((1, output_size))

        # Cache for backpropagation
        self.inputs = None
        self.z = None  # Pre-activation
        self.output = None

        # Gradients
        self.dweights = None
        self.dbiases = None

    def forward(self, inputs: np.ndarray) -> np.ndarray:
        """Forward propagation"""
        self.inputs = inputs
        self.z = np.dot(inputs, self.weights) + self.biases

        # Apply activation
        if self.activation == ActivationFunction.RELU:
            self.output = Activation.relu(self.z)
        elif self.activation == ActivationFunction.SIGMOID:
            self.output = Activation.sigmoid(self.z)
        elif self.activation == ActivationFunction.TANH:
            self.output = Activation.tanh(self.z)
        elif self.activation == ActivationFunction.SOFTMAX:
            self.output = Activation.softmax(self.z)
        else:  # LINEAR
            self.output = Activation.linear(self.z)

        return self.output

    def backward(self, output_gradient: np.ndarray, learning_rate: float) -> np.ndarray:
        """Backward propagation"""

        # Compute activation derivative
        if self.activation == ActivationFunction.RELU:
            activation_grad = Activation.relu_derivative(self.z)
        elif self.activation == ActivationFunction.SIGMOID:
            activation_grad = Activation.sigmoid_derivative(self.z)
        elif self.activation == ActivationFunction.TANH:
            activation_grad = Activation.tanh_derivative(self.z)
        elif self.activation == ActivationFunction.SOFTMAX:
            # For softmax with cross-entropy, gradient is simplified
            activation_grad = np.ones_like(self.z)
        else:  # LINEAR
            activation_grad = Activation.linear_derivative(self.z)

        # Delta = gradient * activation_derivative
        delta = output_gradient * activation_grad

        # Compute gradients
        self.dweights = np.dot(self.inputs.T, delta)
        self.dbiases = np.sum(delta, axis=0, keepdims=True)

        # Gradient for previous layer
        input_gradient = np.dot(delta, self.weights.T)

        return input_gradient


class NeuralNetwork:
    """
    Feedforward neural network with backpropagation

    Features:
    - Multiple layers
    - Different activation functions
    - Various loss functions
    - Mini-batch training
    - Validation during training
    - Model save/load
    """

    def __init__(self):
        self.layers: List[Layer] = []
        self.loss_function = LossFunction.MSE
        self.training_history: List[TrainingMetrics] = []

    def add_layer(
        self,
        output_size: int,
        activation: ActivationFunction = ActivationFunction.RELU
    ):
        """
        Add a layer to the network

        Args:
            output_size: Number of neurons in this layer
            activation: Activation function
        """

        if len(self.layers) == 0:
            raise ValueError("Must specify input_size for first layer using add_input_layer()")

        input_size = self.layers[-1].output_size
        layer = Layer(input_size, output_size, activation)
        self.layers.append(layer)

    def add_input_layer(
        self,
        input_size: int,
        output_size: int,
        activation: ActivationFunction = ActivationFunction.RELU
    ):
        """Add the first layer (with input size specified)"""
        layer = Layer(input_size, output_size, activation)
        self.layers.append(layer)

    def forward(self, X: np.ndarray) -> np.ndarray:
        """Forward propagation through all layers"""

        output = X
        for layer in self.layers:
            output = layer.forward(output)

        return output

    def _compute_loss(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray
    ) -> Tuple[float, np.ndarray]:
        """
        Compute loss and its gradient

        Returns:
            (loss_value, loss_gradient)
        """

        if self.loss_function == LossFunction.MSE:
            # Mean Squared Error
            loss = np.mean((y_pred - y_true) ** 2)
            gradient = 2 * (y_pred - y_true) / y_true.shape[0]

        elif self.loss_function == LossFunction.BINARY_CROSSENTROPY:
            # Binary Cross-Entropy
            y_pred = np.clip(y_pred, 1e-7, 1 - 1e-7)  # Avoid log(0)
            loss = -np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))
            gradient = (y_pred - y_true) / (y_pred * (1 - y_pred) + 1e-7) / y_true.shape[0]

        elif self.loss_function == LossFunction.CATEGORICAL_CROSSENTROPY:
            # Categorical Cross-Entropy
            y_pred = np.clip(y_pred, 1e-7, 1 - 1e-7)
            loss = -np.mean(np.sum(y_true * np.log(y_pred), axis=1))
            gradient = (y_pred - y_true) / y_true.shape[0]

        return loss, gradient

    def backward(self, loss_gradient: np.ndarray, learning_rate: float):
        """Backpropagation through all layers"""

        gradient = loss_gradient

        for layer in reversed(self.layers):
            gradient = layer.backward(gradient, learning_rate)

    def update_weights(self, learning_rate: float):
        """Update weights using computed gradients"""

        for layer in self.layers:
            layer.weights -= learning_rate * layer.dweights
            layer.biases -= learning_rate * layer.dbiases

    def train(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        epochs: int = 100,
        learning_rate: float = 0.01,
        batch_size: int = 32,
        validation_data: Optional[Tuple[np.ndarray, np.ndarray]] = None,
        verbose: bool = True
    ):
        """
        Train the neural network

        Args:
            X_train: Training inputs
            y_train: Training targets
            epochs: Number of epochs
            learning_rate: Learning rate
            batch_size: Mini-batch size
            validation_data: Optional (X_val, y_val) tuple
            verbose: Print progress
        """

        n_samples = X_train.shape[0]
        start_time = time.time()

        for epoch in range(epochs):
            epoch_start = time.time()

            # Shuffle data
            indices = np.random.permutation(n_samples)
            X_shuffled = X_train[indices]
            y_shuffled = y_train[indices]

            # Mini-batch training
            epoch_loss = 0
            n_batches = (n_samples + batch_size - 1) // batch_size

            for i in range(n_batches):
                start_idx = i * batch_size
                end_idx = min((i + 1) * batch_size, n_samples)

                X_batch = X_shuffled[start_idx:end_idx]
                y_batch = y_shuffled[start_idx:end_idx]

                # Forward pass
                y_pred = self.forward(X_batch)

                # Compute loss
                loss, loss_grad = self._compute_loss(y_batch, y_pred)
                epoch_loss += loss

                # Backward pass
                self.backward(loss_grad, learning_rate)

                # Update weights
                self.update_weights(learning_rate)

            # Average loss
            epoch_loss /= n_batches

            # Compute accuracy
            y_pred_train = self.predict(X_train)
            train_accuracy = self._compute_accuracy(y_train, y_pred_train)

            # Validation
            val_loss = None
            val_accuracy = None
            if validation_data:
                X_val, y_val = validation_data
                y_pred_val = self.predict(X_val)
                val_loss, _ = self._compute_loss(y_val, y_pred_val)
                val_accuracy = self._compute_accuracy(y_val, y_pred_val)

            # Record metrics
            metrics = TrainingMetrics(
                epoch=epoch + 1,
                train_loss=epoch_loss,
                train_accuracy=train_accuracy,
                val_loss=val_loss,
                val_accuracy=val_accuracy,
                time_elapsed=time.time() - start_time
            )
            self.training_history.append(metrics)

            # Print progress
            if verbose and (epoch + 1) % max(1, epochs // 10) == 0:
                val_str = ""
                if validation_data:
                    val_str = f", val_loss: {val_loss:.4f}, val_acc: {val_accuracy:.4f}"

                print(f"Epoch {epoch + 1}/{epochs} - "
                      f"loss: {epoch_loss:.4f}, acc: {train_accuracy:.4f}{val_str} "
                      f"({time.time() - epoch_start:.2f}s)")

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions"""
        return self.forward(X)

    def _compute_accuracy(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """Compute classification accuracy"""

        # Handle different output formats
        if y_true.ndim == 1 or y_true.shape[1] == 1:
            # Binary classification
            predictions = (y_pred > 0.5).astype(int).flatten()
            true_labels = y_true.flatten()
        else:
            # Multi-class classification
            predictions = np.argmax(y_pred, axis=1)
            true_labels = np.argmax(y_true, axis=1)

        return np.mean(predictions == true_labels)

    def save_model(self, filepath: str):
        """Save model to file"""

        model_data = {
            'architecture': [
                {
                    'input_size': layer.input_size,
                    'output_size': layer.output_size,
                    'activation': layer.activation.value
                }
                for layer in self.layers
            ],
            'weights': [layer.weights.tolist() for layer in self.layers],
            'biases': [layer.biases.tolist() for layer in self.layers],
            'loss_function': self.loss_function.value
        }

        with open(filepath, 'w') as f:
            json.dump(model_data, f)

    def load_model(self, filepath: str):
        """Load model from file"""

        with open(filepath, 'r') as f:
            model_data = json.load(f)

        # Reconstruct architecture
        self.layers = []
        for i, layer_config in enumerate(model_data['architecture']):
            layer = Layer(
                layer_config['input_size'],
                layer_config['output_size'],
                ActivationFunction(layer_config['activation'])
            )

            # Load weights and biases
            layer.weights = np.array(model_data['weights'][i])
            layer.biases = np.array(model_data['biases'][i])

            self.layers.append(layer)

        self.loss_function = LossFunction(model_data['loss_function'])


def demo_xor():
    """Demonstrate neural network learning XOR function"""

    print("=" * 60)
    print("NEURAL NETWORK - XOR DEMO")
    print("=" * 60)
    print()

    # XOR dataset
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    y = np.array([[0], [1], [1], [0]])

    print("Training neural network to learn XOR...")
    print("Input data:")
    for i in range(len(X)):
        print(f"  {X[i]} -> {y[i][0]}")
    print()

    # Create network
    nn = NeuralNetwork()
    nn.add_input_layer(2, 4, ActivationFunction.TANH)  # Hidden layer
    nn.add_layer(1, ActivationFunction.SIGMOID)        # Output layer
    nn.loss_function = LossFunction.BINARY_CROSSENTROPY

    # Train
    nn.train(X, y, epochs=1000, learning_rate=0.5, batch_size=4, verbose=False)

    # Test
    print("Results after training:")
    predictions = nn.predict(X)
    for i in range(len(X)):
        pred = predictions[i][0]
        print(f"  {X[i]} -> {pred:.4f} (target: {y[i][0]})")

    print()
    accuracy = nn._compute_accuracy(y, predictions)
    print(f"Accuracy: {accuracy * 100:.1f}%")
    print()


def demo_classification():
    """Demonstrate multi-class classification"""

    print("=" * 60)
    print("NEURAL NETWORK - CLASSIFICATION DEMO")
    print("=" * 60)
    print()

    # Generate synthetic data (3 classes)
    np.random.seed(42)
    n_samples = 300

    # Class 0: center at (0, 0)
    X0 = np.random.randn(n_samples // 3, 2) * 0.5
    y0 = np.array([[1, 0, 0]] * (n_samples // 3))

    # Class 1: center at (3, 3)
    X1 = np.random.randn(n_samples // 3, 2) * 0.5 + np.array([3, 3])
    y1 = np.array([[0, 1, 0]] * (n_samples // 3))

    # Class 2: center at (3, 0)
    X2 = np.random.randn(n_samples // 3, 2) * 0.5 + np.array([3, 0])
    y2 = np.array([[0, 0, 1]] * (n_samples // 3))

    # Combine
    X = np.vstack([X0, X1, X2])
    y = np.vstack([y0, y1, y2])

    # Shuffle
    indices = np.random.permutation(n_samples)
    X = X[indices]
    y = y[indices]

    # Split train/test
    split = int(0.8 * n_samples)
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    print(f"Training set: {X_train.shape[0]} samples")
    print(f"Test set: {X_test.shape[0]} samples")
    print(f"Classes: 3")
    print()

    # Create network
    nn = NeuralNetwork()
    nn.add_input_layer(2, 8, ActivationFunction.RELU)
    nn.add_layer(8, ActivationFunction.RELU)
    nn.add_layer(3, ActivationFunction.SOFTMAX)
    nn.loss_function = LossFunction.CATEGORICAL_CROSSENTROPY

    # Train
    print("Training...")
    nn.train(
        X_train, y_train,
        epochs=200,
        learning_rate=0.01,
        batch_size=32,
        validation_data=(X_test, y_test),
        verbose=True
    )

    # Test
    y_pred = nn.predict(X_test)
    test_accuracy = nn._compute_accuracy(y_test, y_pred)

    print()
    print(f"Final test accuracy: {test_accuracy * 100:.1f}%")
    print()


def demo():
    """Run all neural network demos"""

    demo_xor()
    demo_classification()

    print("=" * 60)
    print("NEURAL NETWORK DEMO COMPLETE")
    print("=" * 60)
    print()
    print("Demonstrated:")
    print("1. XOR problem (non-linearly separable)")
    print("2. Multi-class classification")
    print("3. Backpropagation learning")
    print("4. Different activation functions")
    print()
    print("Applications for Consciousness Revolution:")
    print("- Pattern classification")
    print("- Behavior prediction")
    print("- Manipulation detection")
    print("- User profiling")
    print()


if __name__ == "__main__":
    demo()
