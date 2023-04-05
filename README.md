# Flappy Bird AI

This repository contains the source code for an AI that learns to play the popular game Flappy Bird using a deep reinforcement learning algorithm, specifically the NEAT (NeuroEvolution of Augmenting Topologies) algorithm. The goal of this project is to create an AI agent capable of playing Flappy Bird efficiently and autonomously.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [How it Works](#how-it-works)
- [Customization](#customization)
- [License](#license)

## Requirements

- Python 3.7 or higher
- Pygame
- NEAT-Python

## Installation

1. Clone the repository:

```bash
git clone https://github.com/SaidChihabi/Flappy-Bird-AI.git
cd Flappy-Bird-AI
```


2. Install the required dependencies:

```pip install -r requirements.txt```

## Usage

To run the Flappy Bird AI, simply execute the following command from the root directory of the repository:

```python main.py```

The AI will start learning to play Flappy Bird in a new window. You can observe the progress of the algorithm as it evolves and optimizes the neural network.

## How it Works

The NEAT algorithm is used to evolve a population of neural networks. Each network represents an AI agent that tries to play Flappy Bird. During each generation, the neural networks are evaluated based on their performance in the game. The best networks are then selected to reproduce and create the next generation, with small mutations applied to encourage exploration and innovation.

Over time, the AI agents learn to make better decisions based on the game state (e.g., the bird's position and the position of the upcoming pipes), ultimately resulting in a high-performing agent capable of playing the game autonomously.

## Customization

You can customize the behavior of the AI and the NEAT algorithm by modifying the configuration file config-feedforward.txt. This file contains various parameters, such as the population size, the activation functions, and the mutation rates. Adjusting these parameters can result in different learning behaviors and performance.

## License

This project is licensed under the MIT License. See the LICENSE file for more information.

