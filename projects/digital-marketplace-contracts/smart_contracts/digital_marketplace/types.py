import typing
from algopy import UInt64, arc4


class SaleKey(arc4.Struct, frozen=True):
    owner: arc4.Address
    asset: arc4.UInt64


class Bid(arc4.Struct, frozen=True):
    bidder: arc4.Address
    amount: arc4.UInt64


class Sale(arc4.Struct, frozen=True):
    amount: arc4.UInt64
    cost: arc4.UInt64
    # Ideally we'd like to write:
    #  bid: Optional[Bid]
    # Since there's no Optional in Algorand Python, we use the truthiness of bid.bidder
    # to know if a bid is present
    bid: Bid


class BidReceipt(arc4.Struct, frozen=True):
    sale_key: SaleKey
    amount: arc4.UInt64


class UnencumberedBidsReceipt(typing.NamedTuple):
    total_bids: UInt64
    unencumbered_bids: UInt64