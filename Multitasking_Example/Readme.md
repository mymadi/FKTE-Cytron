---

# Handling Interrupts with `countio`

CircuitPython provides **`countio`**, a native module that counts rising-edge and/or falling-edge pin transitions. Internally, `countio` uses interrupts or other hardware mechanisms to catch these transitions and increment a count.

You can use `countio` with `asyncio` to catch interrupts and do something based on that interrupt. Here is a simple example using `countio` to monitor a pin connected to a push button, which will simulate a device interrupt. Note that the `countio` value is being polled in the task.

<hr></hr>

# Cooperative Multitasking in CircuitPython with `asyncio`

## Overview

This guide describes how to do cooperative multitasking in CircuitPython, using the `asyncio` library and the `async` and `await` language keywords. The `asyncio` library is included with CPython, the host-computer version of Python. MicroPython also supplies a version of `asyncio`, and that version has been adapted for use in CircuitPython.

<hr></hr>

# pyRTOS: A Pure Python Real-Time Operating System

## Introduction

This project utilizes **pyRTOS**, a Real-Time Operating System (RTOS) written entirely in Python. Its main purpose is to offer an RTOS solution that seamlessly integrates with **CircuitPython** environments, making it an ideal educational tool for advanced CircuitPython users eager to delve into RTOS concepts. Beyond CircuitPython, `pyRTOS` is also designed to be compatible with **MicroPython** and can even be used in standard Python.

## Key Characteristics & Differences

`pyRTOS` draws inspiration from the well-known FreeRTOS, but it incorporates some notable distinctions:

* **Voluntary Task Preemption:** Unlike FreeRTOS, which typically enforces task preemption using timer interrupts, `pyRTOS` employs a **voluntary task preemption model**. This means that tasks must explicitly yield control to the scheduler. This design places a greater responsibility on the user to ensure tasks are "well-behaved" and periodically give up the processor, preventing any single task from monopolizing CPU time.
* **Naming Conventions:** `pyRTOS` uses its own set of naming conventions.
* **Built-in Message Passing:** `pyRTOS` includes built-in mechanisms for inter-task message passing, facilitating communication between different concurrent tasks.

<hr></hr>

## Reference

1.  **FreeRTOS:** [https://www.freertos.org/](https://www.freertos.org/)]
2.  **pyRTOS GitHub Repository:** [https://github.com/Rybec/pyRTOS](https://github.com/Rybec/pyRTOS)]
3.  **Concurrent Tasks:** [https://learn.adafruit.com/cooperative-multitasking-in-circuitpython-with-asyncio/concurrent-tasks]
4.  **Handling Interrupts:** [https://learn.adafruit.com/cooperative-multitasking-in-circuitpython-with-asyncio/handling-interrupts]
