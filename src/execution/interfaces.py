# src/execution/interfaces.py
# Defines the standard interfaces for all execution and brokerage modules.

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Literal, List

@dataclass
class OrderRequest:
    """
    The standardized data structure for an order request.
    This is the "nerve signal" sent from ARMS modules to the execution layer.
    
    Based on FSD v1.1, Section 8.3.
    """
    ticker: str
    action: Literal['BUY', 'SELL', 'BUY_PUT', 'SELL_CALL']
    quantity: float  # Use float to handle notional orders for things like puts
    order_type: Literal['MARKET', 'VWAP', 'LIMIT']
    
    # Context from the system
    triggering_module: str
    triggering_signal: str
    tier: int

@dataclass
class Position:
    """
    A standardized representation of a portfolio position.
    """
    ticker: str
    quantity: float
    average_cost: float
    market_value: float

class Broker(ABC):
    """
    An abstract base class that defines the standard interface for any broker.
    Any broker implementation (e.g., for IBKR, Alpaca) must implement these methods.
    """

    @abstractmethod
    def connect(self):
        """Establish a connection to the broker."""
        pass

    @abstractmethod
    def disconnect(self):
        """Terminate the connection to the broker."""
        pass

    @abstractmethod
    def submit_order(self, order: OrderRequest) -> str:
        """
        Submits an order to the broker.
        
        Returns:
            A unique order ID from the broker.
        """
        pass

    @abstractmethod
    def get_positions(self) -> List[Position]:
        """
        Retrieves the current portfolio positions from the broker.
        """
        pass

    @abstractmethod
    def get_order_status(self, order_id: str) -> Literal['PENDING', 'FILLED', 'FAILED', 'CANCELLED']:
        """
        Checks the status of a previously submitted order.
        """
        pass
