# DC Bot - teraltc

> A Discord bot tailored for cryptocurrency enthusiasts, built with discord.py (PyCord), focusing on slash commands for a streamlined experience.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Slash Commands](#slash-commands)
- [Contributing](#contributing)
- [License](#license)

---

## Introduction

DC Bot is a feature-packed Discord bot focused on the world of cryptocurrency. It leverages discord.py (PyCord) to provide a streamlined experience through slash commands. Users can effortlessly interact with various aspects of the crypto universe, from checking live Litecoin prices to setting custom exchange rates. With additional features like fiat exchange rate checks, Litecoin balance verification, and the ability to confirm transactions using a hash, DC Bot is your go-to companion for staying updated on all things crypto.
---

## Features

- View live Litecoin prices
- Set custom INR to crypto and crypto to INR rates in USD or INR
- Check fiat exchange rates between INR and USD
- Verify Litecoin balances using addresses
- Confirm Litecoin transactions using a hash
- Extract a hash from a transaction URL
- Calculate given expressions
---

## Getting Started

To get started with DC Bot, follow these simple steps:

1. Clone the repository
2. Install the necessary dependencies
3. Configure your Discord bot token and API keys
4. Run the bot

For detailed instructions, refer to the [Getting Started Guide](docs/getting-started.md).

---

## Usage

Once the bot is up and running, you can interact with it directly in your Discord server. Use the slash commands listed below to access the respective functionalities.

---

## Slash Commands

- `/set_i2c`: Set the rate of INR to crypto
- `/i2c`: Get the INR to crypto perfect rate by entering INR
- `/set_c2i`: Set the rate of crypto to INR
- `/c2i`: Get the crypto to INR perfect rate by entering INR
- `/ltcp`: Get the LTC price
- `/checkbal`: Use this command to enter your LTC address and get your wallet balance
- `/extracthash`: Get the hash from any transaction URL
- `/checkconfirmations`: Get full details about a transaction using its hash
- `/calculate`: Perform a calculation (Usage: `/calculate [operation] [num1] [num2]`)
- `/currencyexchange`: Get the exchange rate for fiat currencies (Not related to crypto)

For more detailed usage instructions, refer to the [Commands Guide](docs/commands.md).

---

## Contributing

We welcome contributions from the community! If you'd like to contribute to the project, please read our [Contributing Guidelines](CONTRIBUTING.md).

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

