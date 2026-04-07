"""
ARMS Execution: Order Book & Liquidity-Adjusted Execution Protocol (LAEP)

This is the L5 execution core. It receives OrderRequests from the engine,
evaluates the current VIX (Liquidity Mode), and translates the requests
into actionable broker instructions with enforced execution windows,
slippage budgets, and priority ordering.

Reference: THB v4.0, Section 5
"""
from dataclasses import dataclass
from typing import List, Literal
from enum import Enum

from .order_request import OrderRequest
from reporting.audit_log import SessionLogEntry, append_to_log
import datetime

class LiquidityMode(Enum):
    NORMAL = "NORMAL"   # VIX < 25
    ELEVATED = "ELEVATED" # VIX 25-45
    CRISIS = "CRISIS"   # VIX > 45

@dataclass
class OrderBookEntry:
    """
    Extended representation of an order ready for broker submission.
    Incorporates LAEP dynamic constraints.
    """
    request: OrderRequest
    liquidity_mode: LiquidityMode
    order_type: Literal['MARKET', 'VWAP', 'LIMIT']
    execution_window_min: int
    slippage_budget_bps: float
    priority: int

class OrderBook:
    """
    Manages the translation and staging of OrderRequests before they hit the broker.
    """
    def __init__(self):
        self.queue: List[OrderBookEntry] = []

    def _determine_liquidity_mode(self, current_vix: float) -> LiquidityMode:
        if current_vix < 25:
            return LiquidityMode.NORMAL
        elif current_vix <= 45:
            return LiquidityMode.ELEVATED
        else:
            return LiquidityMode.CRISIS

    def process_request(self, request: OrderRequest, current_vix: float) -> OrderBookEntry:
        """
        Applies LAEP rules to a raw OrderRequest based on current market volatility.
        """
        mode = self._determine_liquidity_mode(current_vix)
        
        # Base translation from request
        order_type = request.order_type
        window = request.execution_window_min
        slippage = request.slippage_budget_bps
        priority = request.priority

        # LAEP Overrides (THB v4.0 Section 5.1)
        if mode == LiquidityMode.NORMAL:
            if order_type == 'MARKET':
                window = 30
                slippage = 8.0
        elif mode == LiquidityMode.ELEVATED:
            # Force VWAP in elevated vol
            if order_type == 'MARKET':
                order_type = 'VWAP'
            window = max(window, 60)
            slippage = max(slippage, 20.0)
        elif mode == LiquidityMode.CRISIS:
            # Force VWAP and extend window in crisis
            if order_type == 'MARKET':
                order_type = 'VWAP'
            window = max(window, 90)
            slippage = max(slippage, 40.0)

            # Crisis Priority Reorder: Illiquid crypto exits first
            if request.action == 'SELL':
                if request.ticker == 'BSOL': priority = 1
                elif request.ticker == 'ETHB': priority = 2
                elif request.ticker == 'IBIT': priority = 3
                else: priority = 4 # Equities last

        entry = OrderBookEntry(
            request=request,
            liquidity_mode=mode,
            order_type=order_type,
            execution_window_min=window,
            slippage_budget_bps=slippage,
            priority=priority
        )
        
        self.queue.append(entry)
        
        append_to_log(SessionLogEntry(
            timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            action_type='LAEP_EVALUATION',
            triggering_module='ORDER_BOOK',
            triggering_signal=f"LAEP {mode.value}: Translated {request.action} {request.ticker} to {order_type} (Win: {window}m, Slip: {slippage}bps, Pri: {priority})",
            correlation_id=request.correlation_id,
            ticker=request.ticker
        ))
        
        return entry

    def get_executable_batch(self) -> List[OrderBookEntry]:
        """
        Returns the sorted queue ready for the broker, respecting priority.
        Priority 1 executes before Priority 4.
        """
        # Sort by priority (lower number = higher priority)
        batch = sorted(self.queue, key=lambda x: x.priority)
        self.queue = [] # Clear queue after handing off to broker
        return batch
