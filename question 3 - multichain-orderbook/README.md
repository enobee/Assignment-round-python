# Question 3 - Multichain Orderbook System Design

A decentralized orderbook system for cross-chain asset trading that enables users to place and fill orders for assets across different blockchains.

## Overview

This system manages a multichain orderbook that allows trading of any asset pair across two different blockchains. It implements a maker/taker model with careful consideration for gas costs, liquidity challenges, and execution speed.

### Key Features

- **Cross-Chain Trading**: Trade assets between different blockchains
- **Order Book Model**: Traditional limit order book with price-time priority
- **Gas Handling**: Optimizes for gas costs across multiple chains
- **Liquidity Management**: Flexible policies for handling partial fills
- **Health Monitoring**: Continuous monitoring of all system components

## System Architecture

The system is composed of several key components:

### Core Models

- **Blockchain**: Represents a specific blockchain with its properties and gas estimation logic
- **Asset**: Represents a tradable asset that exists on one or more blockchains
- **Order**: Represents buy/sell orders with their properties and status
- **OrderMatch**: Represents a match between a taker order and maker orders

### Orderbook Components

- **OrderBookPair**: Manages orders for a specific trading pair
- **MultiChainOrderBook**: Central component managing all trading pairs

### Execution Components

- **CrossChainManager**: Orchestrates cross-chain transactions
- **EthereumBridge**: Implements cross-chain transfers for Ethereum-compatible chains

### Supporting Components

- **SystemConfig**: Configuration for timeouts, confirmations, etc.
- **EventBus**: Publish-subscribe system for internal communication
- **Logger**: Structured logging system
- **HealthMonitor**: Monitors system and blockchain health
- **GasEstimator**: Estimates gas costs across chains

### Storage Components

- **OrderRepository**: Stores and retrieves orders
- **MatchRepository**: Stores and retrieves matches

## Addressing Key Constraints

### Immediate Order Fulfillment

Taker orders are processed immediately with optimized gas prices to ensure inclusion in the next block.

### Liquidity Challenges

The system can be configured to:

- Reject orders that cannot be completely filled
- Partially fill orders with available liquidity
- Fill what's available and convert the remainder to a maker order

### Gas Fee Consideration

Every transaction evaluates gas costs across all involved blockchains:

- Gas estimations account for current network conditions
- Trades are only executed if gas costs are reasonable compared to trade value
- Different operations use appropriate gas price strategies

## How It Works

1. **Setup**: The system initializes with supported blockchains, assets, and bridges
2. **Order Placement**: Users can submit maker orders (limit orders) or taker orders (market orders)
3. **Order Matching**: Taker orders are matched against the best available maker orders
4. **Cross-Chain Execution**:
   - Assets are locked on source chains
   - Proofs of locks are generated
   - Assets are released on destination chains
5. **Status Updates**: Order statuses are updated and events are published

## Design Principles

- **Separation of Concerns**: Each component has a clear responsibility
- **Fail-Safe Execution**: Cross-chain transfers use an atomic pattern with rollback capability
- **Configurability**: System behavior can be adjusted through configuration
- **Health Awareness**: All components are monitored for proper functioning

## License

MIT
