# Construct Quantum Neural Network using [Tensorflow-quantum](https://www.tensorflow.org/quantum/overview) or [Qiskit](https://qiskit.org/textbook/ch-machine-learning/machine-learning-qiskit-pytorch.html#quantumlayer)

## 1. How to run
- Checkout
```
pip install quhep
```
quhep_tfq -i data/qml/hmumu_twojet_0719.npy --nqubits 3 --batch-size 4  --training-size 4 --val-size 4 --test-size 4 --epochs 1 --loss mse use_quple
