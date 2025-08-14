# Digital Marketplace Smart Contract

This example demonstrates a Digital Marketplace smart contract on Algorand. It allows users to list assets for sale, either for a fixed price or through an auction-style bidding system.

## Features

- **Deposits:** Users can deposit and withdraw ALGOs into the contract to be used for purchases and bids.
- **Asset Sales:** Users can list their assets (ASAs) for sale at a fixed price.
- **Bidding:** For assets on sale, users can place bids. A new bid must be higher than the current highest bid.
- **Purchases:** A buyer can purchase a listed asset directly if a fixed price is set.
- **Auctions:** Sellers can accept the highest bid on their asset, transferring the asset to the bidder and the bid amount to the seller.
- **Bid Management:** Bidders can withdraw their bids if they are not the leading bid on any auction.

## How it works

The contract manages user balances in a `BoxMap` and keeps track of sales and bids.

### Key Functions

- `deposit(payment: gtxn.PaymentTransaction)`: Deposits ALGOs into the user's account within the contract.
- `withdraw(amount: arc4.UInt64)`: Withdraws a specified amount of ALGOs from the user's account.
- `open_sale(asset_deposit: gtxn.AssetTransferTransaction, cost: arc4.UInt64)`: Creates a new sale for an asset at a given `cost`.
- `close_sale(asset: Asset)`: Allows the seller to close their sale and reclaim their asset.
- `buy(sale_key: SaleKey)`: Allows a user to buy an asset for the specified `cost`.
- `bid(sale_key: SaleKey, new_bid_amount: arc4.UInt64)`: Places a bid on an asset. The bid must be higher than the current one.
- `accept_bid(asset: arc4.UInt64)`: The seller accepts the highest bid. The asset is transferred to the bidder, and the funds are transferred to the seller.
- `claim_unencumbered_bids()`: Allows a user to recover funds from bids that are no longer active or winning.

