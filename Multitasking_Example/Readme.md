# pyRTOS: A Pure Python Real-Time Operating System

## Introduction

This project utilizes **pyRTOS**, a Real-Time Operating System (RTOS) written entirely in Python. Its main purpose is to offer an RTOS solution that seamlessly integrates with **CircuitPython** environments, making it an ideal educational tool for advanced CircuitPython users eager to delve into RTOS concepts. Beyond CircuitPython, `pyRTOS` is also designed to be compatible with **MicroPython** and can even be used in standard Python.

## Key Characteristics & Differences

`pyRTOS` draws inspiration from the well-known FreeRTOS, but it incorporates some notable distinctions:

* **Voluntary Task Preemption:** Unlike FreeRTOS, which typically enforces task preemption using timer interrupts, `pyRTOS` employs a **voluntary task preemption model**. This means that tasks must explicitly yield control to the scheduler. This design places a greater responsibility on the user to ensure tasks are "well-behaved" and periodically give up the processor, preventing any single task from monopolizing CPU time.
* **Naming Conventions:** `pyRTOS` uses its own set of naming conventions.
* **Built-in Message Passing:** `pyRTOS` includes built-in mechanisms for inter-task message passing, facilitating communication between different concurrent tasks.

## Reference

1.  **FreeRTOS:** [https://www.freertos.org/](https://www.freertos.org/)
2.  **pyRTOS GitHub Repository:** [https://github.com/Rybec/pyRTOS](https://github.com/Rybec/pyRTOS)
