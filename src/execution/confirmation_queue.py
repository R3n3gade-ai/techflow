# src/execution/confirmation_queue.py
# Implements the Tier 1 Confirmation Queue with the information-quality interface.

from dataclasses import dataclass, field
from typing import List, Literal, Optional
from datetime import datetime, timedelta

# We need the OrderRequest to represent what is being approved
# This will be in its own file, but we can define a placeholder for now.
# from .interfaces import OrderRequest 
@dataclass
class PlaceholderOrderRequest:
    ticker: str
    action: str

@dataclass
class QueuedAction:
    """
    Represents a single Tier 1 action waiting for PM confirmation.
    """
    action_id: str
    item: PlaceholderOrderRequest  # The actual order or action being requested
    triggering_module: str
    rationale: str
    queued_at: datetime
    veto_window_hours: float
    
    status: Literal['PENDING', 'EXECUTED', 'HELD', 'VETOED', 'TIMED_OUT'] = 'PENDING'
    pm_rationale: Optional[str] = None

class ConfirmationQueue:
    """
    Manages the queue of Tier 1 actions that require PM review.
    """
    
    def __init__(self):
        self._queue: List[QueuedAction] = []

    def add_action(self, action: QueuedAction):
        """Adds a new Tier 1 action to the queue."""
        print(f"[ConfirmationQueue] New Tier 1 Action added: {action.action_id}")
        self._queue.append(action)

    def get_open_items(self) -> List[QueuedAction]:
        """Returns all actions currently in a 'PENDING' state."""
        return [action for action in self._queue if action.status == 'PENDING']

    def submit_response(self, action_id: str, response: Literal['EXECUTE', 'HOLD', 'VETO'], rationale: Optional[str] = None):
        """
        Submits a PM's response to a queued action.
        """
        action = next((a for a in self._queue if a.action_id == action_id), None)
        if not action or action.status != 'PENDING':
            print(f"[ConfirmationQueue] Action {action_id} not found or already actioned.")
            return

        if response == 'VETO' and not rationale:
            print("[ConfirmationQueue] VETO response requires a rationale.")
            return

        action.status = f"{response}ED" # e.g., EXECUTED, VETOED
        action.pm_rationale = rationale
        print(f"[ConfirmationQueue] PM responded to {action_id} with: {response}")

    def check_for_timeouts(self):
        """
        Checks for actions where the veto window has expired and marks them
        for automatic execution.
        
        This would be called periodically by the scheduler.
        """
        now = datetime.utcnow()
        for action in self.get_open_items():
            expiry_time = action.queued_at + timedelta(hours=action.veto_window_hours)
            if now >= expiry_time:
                action.status = 'TIMED_OUT'
                print(f"[ConfirmationQueue] Action {action.action_id} timed out. Proceeding with default execution.")

# The main application would then have logic to process actions based on their status,
# e.g., sending items with status 'EXECUTED' or 'TIMED_OUT' to the broker_api.
