# src/execution/broker_api.py
# IBKR broker adapter scaffold for ARMS paper-trading integration.

from __future__ import annotations

import logging
from typing import List, Literal, Optional, Tuple

try:
    import ib_insync as ibi
    IB_AVAILABLE = True
except ImportError:
    IB_AVAILABLE = False
    logging.warning("ib_insync not found. Broker API will run in degraded scaffold mode.")

from .interfaces import Broker, Position
from .order_request import OrderRequest


class IBKRBroker(Broker):
    """
    Interactive Brokers adapter using ib_insync.

    Current state:
    - Real connection established if ib_insync is available.
    - Position snapshot implemented.
    - Order submission restricted to paper mode.
    - Option contract resolution (e.g., PTRH puts) is mocked/pending.
    """

    def __init__(
        self,
        host: str = '127.0.0.1',
        port: int = 4002,
        client_id: int = 1,
        paper: bool = True,
        connect_timeout_s: float = 10.0,
    ):
        # Detect if we are inside a docker container bridging to host via SSH tunnel
        # The SSH tunnel forwards local 4002 to VPS localhost 4002.
        self.host = host
        self.port = port
        self.client_id = client_id
        self.paper = paper
        self.connect_timeout_s = connect_timeout_s
        
        self.ib: Optional['ibi.IB'] = None
        self.is_connected = False

        print(
            f"[IBKRBroker] Initialized host={self.host} port={self.port} "
            f"client_id={self.client_id} paper={self.paper}"
        )

    def _require_connection(self):
        if not self.is_connected or not self.ib:
            raise ConnectionError("Broker is not connected.")

    def _paper_guard(self):
        if not self.paper:
            raise RuntimeError(
                "Live trading is not enabled in this adapter path. "
                "Use paper=True until execution hardening is complete."
            )

    def connect(self):
        """Establish connection to IB Gateway / TWS."""
        self._paper_guard()
        
        if not IB_AVAILABLE:
            print("[IBKRBroker] ib_insync unavailable. Simulating connection success.")
            self.is_connected = True
            return

        print(
            f"[IBKRBroker] Connecting to IBKR at {self.host}:{self.port} "
            f"with client_id={self.client_id}..."
        )
        
        try:
            self.ib = ibi.IB()
            self.ib.connect(
                self.host, 
                self.port, 
                clientId=self.client_id, 
                timeout=self.connect_timeout_s
            )
            self.is_connected = self.ib.isConnected()
            
            if self.is_connected:
                print(f"[IBKRBroker] Connected. Managed accounts: {self.ib.managedAccounts()}")
            else:
                print("[IBKRBroker] Connection failed silently.")
                
        except Exception as e:
            self.is_connected = False
            self.ib = None
            print(f"[IBKRBroker] Connection error: {e}")
            raise ConnectionError(f"Failed to connect to IBKR: {e}")

    def disconnect(self):
        if self.is_connected:
            print("[IBKRBroker] Disconnecting...")
            if self.ib:
                self.ib.disconnect()
        self.is_connected = False
        self.ib = None
        print("[IBKRBroker] Disconnected.")

    def get_positions(self) -> List[Position]:
        """Fetch current portfolio positions from the broker."""
        self._require_connection()
        
        if not IB_AVAILABLE or not self.ib:
            print("[IBKRBroker] Position snapshot scaffold invoked (no IB backend).")
            return []
            
        print("[IBKRBroker] Fetching live positions...")
        ib_positions = self.ib.positions()
        
        normalized = []
        for p in ib_positions:
            # Note: market_value and average_cost require deeper portfolio() or accountValues() lookups
            # in ib_insync, but we map what we have immediately from positions().
            normalized.append(Position(
                ticker=p.contract.symbol,
                sec_type=p.contract.secType,
                quantity=float(p.position),
                average_cost=float(p.avgCost),
                market_value=0.0, # Requires live market data or account summary
                con_id=p.contract.conId
            ))
            
        print(f"[IBKRBroker] Retrieved {len(normalized)} positions.")
        return normalized

    def get_nav(self) -> float:
        """Fetch current Net Asset Value from the broker."""
        self._require_connection()
        
        if not IB_AVAILABLE or not self.ib:
            print("[IBKRBroker] NAV scaffold invoked (no IB backend). Returning default $50M.")
            return 50_000_000.0

        print("[IBKRBroker] Fetching live NAV...")
        try:
            # NetLiquidation value is the standard NAV proxy in IBKR
            account_values = self.ib.accountValues()
            for val in account_values:
                if val.tag == 'NetLiquidation' and val.currency == 'USD':
                    nav = float(val.value)
                    print(f"[IBKRBroker] Live NAV retrieved: ${nav:,.2f}")
                    return nav
        except Exception as e:
            print(f"[IBKRBroker] Failed to fetch NAV: {e}. Falling back to default.")
            
        return 50_000_000.0

    def submit_order(self, order: OrderRequest) -> str:
        self._require_connection()
        self._paper_guard()

        # Transitional validation.
        if order.tier == 1 and not order.confirmation_required:
            raise ValueError("Tier 1 orders must set confirmation_required=True.")
        if order.order_type == 'LIMIT' and order.limit_price is None:
            raise ValueError("LIMIT orders require limit_price.")
            
        if not IB_AVAILABLE or not self.ib:
            print(f"[IBKRBroker] Scaffold submit: {order}")
            return f"paper_scaffold_{order.correlation_id}_{order.ticker.lower()}"

        print(f"[IBKRBroker] Preparing live paper order for {order.action} {order.quantity} {order.ticker}")
        
        # 1. Contract Resolution
        if order.action in {'BUY_PUT', 'SELL_PUT', 'SELL_CALL'}:
            # Fallback or fully dynamic contract resolution will go here
            if getattr(order, 'con_id', None):
                contract = ibi.Contract(conId=order.con_id)
            else:
                print("[IBKRBroker] Option contract resolution requires con_id or strike/expiry metadata. Halting submit.")
                raise NotImplementedError("Dynamic option contract scanning is pending implementation in PTRH.")
        else:
            contract = ibi.Stock(order.ticker, 'SMART', 'USD')
            
        # 2. Order Translation
        ib_action = 'BUY' if order.action == 'BUY' else 'SELL'
        
        if order.order_type == 'MARKET':
            ib_order = ibi.MarketOrder(ib_action, float(order.quantity))
        elif order.order_type == 'LIMIT':
            ib_order = ibi.LimitOrder(ib_action, float(order.quantity), float(order.limit_price or 0.0))
        elif order.order_type == 'VWAP':
            # Simplified IBALGO VWAP representation
            ib_order = ibi.Order(
                action=ib_action,
                totalQuantity=float(order.quantity),
                orderType='VWAP',
                algoStrategy='VWAP',
                algoParams=[ibi.TagValue('maxPctVol', '0.1')]
            )
        else:
            raise ValueError(f"Unsupported order type: {order.order_type}")
            
        # 3. Submission
        print(f"[IBKRBroker] Submitting to IBKR: {contract} -> {ib_order}")
        trade = self.ib.placeOrder(contract, ib_order)
        
        # In a real async environment, we wouldn't block here endlessly, but for
        # the synchronous orchestrator we might wait briefly or return the ID immediately.
        
        order_id = f"ibkr_live_{trade.order.orderId}" if trade.order.orderId else f"ibkr_temp_{id(trade)}"
        print(f"[IBKRBroker] Order {order.correlation_id} submitted. Temporary ID: {order_id}")
        return order_id

    def get_order_status(self, order_id: str) -> Literal['PENDING', 'FILLED', 'FAILED', 'CANCELLED']:
        self._require_connection()
        
        if not IB_AVAILABLE or not self.ib:
            print(f"[IBKRBroker] Status scaffold for order_id={order_id}")
            return 'PENDING'
            
        print(f"[IBKRBroker] Checking status for {order_id}...")
        # A full implementation searches self.ib.trades() and maps ib_insync status
        # strings ('Submitted', 'Filled', 'Cancelled', 'Inactive') to our canonical literals.
        return 'PENDING'

    def get_options_chain(self, ticker: str, exchange: str = 'SMART') -> List['ibi.Option']:
        """
        Fetch the current options chain for the given underlying.
        Used by PTRH Adaptive Strike Protocol to find optimal delta contracts.
        """
        self._require_connection()
        if not IB_AVAILABLE or not self.ib:
            print(f"[IBKRBroker] Options chain scaffold invoked for {ticker}. Returning empty.")
            return []

        print(f"[IBKRBroker] Fetching options chain for {ticker}...")
        underlying = ibi.Index(ticker, exchange) if ticker in ['SPX', 'VIX'] else ibi.Stock(ticker, exchange, 'USD')
        self.ib.qualifyContracts(underlying)
        
        chains = self.ib.reqSecDefOptParams(underlying.symbol, '', underlying.secType, underlying.conId)
        if not chains:
            print(f"[IBKRBroker] No options chain returned for {ticker}.")
            return []
            
        chain = next((c for c in chains if c.exchange == exchange), chains[0])
        print(f"[IBKRBroker] Retrieved chain with {len(chain.expirations)} expiries and {len(chain.strikes)} strikes.")
        
        # Build raw option contracts for later filtering and market data request
        contracts = []
        for exp in chain.expirations:
            for strike in chain.strikes:
                contracts.append(ibi.Option(ticker, exp, strike, 'P', exchange))
        
        # Qualify contracts (batch in real life, but here we return raw and let the engine qualify subsets)
        return contracts

    def get_market_data(self, contracts: List['ibi.Contract']) -> List['ibi.Ticker']:
        """
        Fetch a live market data snapshot for a list of contracts.
        Used to calculate Deltas and bid/ask spreads.
        """
        self._require_connection()
        if not IB_AVAILABLE or not self.ib:
            return []
            
        # Ensure we don't overwhelm the API; qualify and request tickers
        qualified = self.ib.qualifyContracts(*contracts)
        tickers = self.ib.reqTickers(*qualified)
        return tickers
