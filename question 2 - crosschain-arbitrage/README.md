# Question 2: Cross-Chain Arbitrage (Arbitrum & Optimism)

This script performs a cross-chain token swap:

- From **USDC to USDT** on **Arbitrum** using **Uniswap V3**
- Then from **USDT to USDC** on **Optimism** using **Curve**

It executes both swaps **simultaneously** using `asyncio` and includes **error handling** for failed transactions.

## Features

- **Swaps USDC -> USDT on Arbitrum via Uniswap V3**
- **Swaps USDT -> USDC on Optimism via Curve**
- Uses smart contract ABIs to interact directly with protocols
- Automatically connects to both chains using `Alchemy` RPCs

---

## Getting Started

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Create a `.env` file in the root directory:

```env
PRIVATE_KEY=your_wallet_private_key
ARBITRUM_RPC=your_alchemy_arbitrum_key
OPTIMISM_RPC=your_alchemy_optimism_key
```

### 3. Run the Script

```bash
python main.py
```

---

## 4. How It Works

### Arbitrum Swap (Uniswap V3)

Swaps 5 USDC for USDT using the `exactInputSingle` function on Uniswap V3.

### Optimism Swap (Curve Finance)

Swaps 5 USDT for USDC using the `exchange(i, j)` method on a Curve pool.

## Error Handling

If a swap fails (e.g. gas issues, network error), it will be caught and logged like this:

```bash
 Uniswap swap failed: <error message>
```

The script will continue running and execute the remaining swap.

### Tokens Used

- Arbitrum:
  - USDC: `0xff970a61a04b1ca14834a43f5de4533ebddb5cc8`
  - USDT: `0xfd086bc7cd5c481dcc9c85ebe478a1c0b69fcbb9`
- Optimism:
  - Token indices are used (i = 2 for USDT, j = 1 for USDC)

### Contracts Used

- Uniswap Router: `0xE592427A0AEce92De3Edee1F18E0157C05861564`
- Curve Pool: `0x45c562b0a4e2efc8768315e4eced54c46041f657`

---

## Bonus Question: What Risks Does This Transaction Pose?

This transaction poses several risks due to its multichain and DeFi nature:

### Multichain Risks

- **Latency Risk/Timing Risk**: There is no guarantee that both transactions will be mined at the same time. If one goes through and the other fail, there will might be loss of money or get stuck with a bad rate.

- **Slippage**: If the price moves after the trade is submitted, there might be worse rates than expected.

- **Front-running**: Bots might see the trade in the mempool and try to beat it.

- **Gas Fees**: Each chain has different gas fees, if they spike suddenly, the profit might be lost.

- **Cross-chain inconsistency**: These are two different chains and there are no built-in coordination. Trades can't be bundled atomically without complex bridging logic.

- **Liquidity Risk**: If there is not enough liquidity in a pool, the trade might fail or have very bad slippage.

## License

MIT
