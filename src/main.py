# src/main.py
# The main application entry point for the Achelion ARMS system.
# This file orchestrates all the different modules.

from datetime import datetime, timezone
from data_feeds.pipeline import DataPipeline
from engine.mics import calculate_mics, SentinelGateInputs
from execution.confirmation_queue import ConfirmationQueue, QueuedAction
from execution.broker_api import IBKRBroker
from reporting.audit_log import SessionLogEntry, append_to_log
from execution.interfaces import OrderRequest

def run_daily_cycle():
    """
    A simplified representation of the main operational loop that ARMS
    would run, demonstrating the integration of the audit log.
    """
    log_file = "achelion_arms/logs/session_log.jsonl"
    print("==================================================")
    print("ACHELION ARMS - DAILY CYCLE START")
    print(f"Logging all actions to: {log_file}")
    print("==================================================")
    append_to_log(SessionLogEntry(timestamp=datetime.now(timezone.utc).isoformat(), action_type='CYCLE_START', triggering_module='main', triggering_signal='Daily cycle initiated.'), log_file)

    # 1. Initialize all core services
    print("\n[1. Initializing Services...]")
    append_to_log(SessionLogEntry(timestamp=datetime.now(timezone.utc).isoformat(), action_type='INITIALIZATION', triggering_module='main', triggering_signal='Initializing all core services.'), log_file)
    data_pipeline = DataPipeline()
    broker = IBKRBroker()
    confirmation_queue = ConfirmationQueue()
    broker.connect()

    # 2. Run the Data Ingestion Pipeline (The Senses)
    print("\n[2. Running Data Ingestion Pipeline...]")
    signals = data_pipeline.run_all_feeds()
    append_to_log(SessionLogEntry(timestamp=datetime.now(timezone.utc).isoformat(), action_type='DATA_INGESTION', triggering_module='DataPipeline', triggering_signal=f'Successfully fetched {len(signals)} signal records.'), log_file)

    # 3. Placeholder for a System Action (The Brain making a decision)
    print("\n[3. Simulating MICS Calculation...]")
    sentinel_data = SentinelGateInputs(
        gate3_raw_score=22, source_category='Cat B', fem_impact='NORMAL->WATCH', regime_at_entry='NEUTRAL'
    )
    mics_result = calculate_mics(sentinel_data)
    print(f" -> MICS Calculation Complete. Result: C-Level {mics_result.conviction_level} (Raw: {mics_result.raw_score:.2f})")
    append_to_log(SessionLogEntry(timestamp=datetime.now(timezone.utc).isoformat(), action_type='MICS_CALCULATION', triggering_module='MICS', triggering_signal='New SENTINEL candidate scored.', mics_score=mics_result.raw_score, gate3_score=22, source_category='Cat B'), log_file)

    # 4. Queue a Tier 1 Action for PM approval
    print("\n[4. Queuing a Tier 1 Action...]")
    order_to_approve = OrderRequest(
        ticker="NVDA", action="BUY", quantity=100, order_type="VWAP",
        triggering_module="SENTINEL", triggering_signal="New position passed all 6 gates.", tier=1
    )
    queued_action = QueuedAction(
        action_id="sentinel_nvda_buy_001", item=order_to_approve, triggering_module="SENTINEL",
        rationale="New position passed all gates, awaiting PM confirmation.", queued_at=datetime.now(timezone.utc), veto_window_hours=4.0
    )
    confirmation_queue.add_action(queued_action)
    append_to_log(SessionLogEntry(timestamp=datetime.now(timezone.utc).isoformat(), action_type='TIER1_ACTION_QUEUED', triggering_module='SENTINEL', triggering_signal=f'Queued action {queued_action.action_id} for {order_to_approve.ticker}.', ticker=order_to_approve.ticker), log_file)

    # 5. Check the Confirmation Queue (The Dashboard)
    print("\n[5. Checking for Open Actions...]")
    open_items = confirmation_queue.get_open_items()
    print(f" -> Found {len(open_items)} open action(s) for PM review.")

    # 6. Simulate a PM response and execute
    print("\n[6. Simulating PM Approval and Execution...]")
    if open_items:
        action_id = open_items[0].action_id
        confirmation_queue.submit_response(action_id, 'EXECUTE')
        append_to_log(SessionLogEntry(timestamp=datetime.now(timezone.utc).isoformat(), action_type='PM_CONFIRMATION', triggering_module='ConfirmationQueue', triggering_signal=f'PM confirmed action {action_id} with response EXECUTE.'), log_file)
        
        order_to_execute = open_items[0].item
        order_id = broker.submit_order(order_to_execute)
        append_to_log(SessionLogEntry(timestamp=datetime.now(timezone.utc).isoformat(), action_type='ORDER_SUBMITTED', triggering_module='BrokerAPI', triggering_signal=f'Broker order {order_id} submitted.', ticker=order_to_execute.ticker), log_file)

    # 7. Disconnect and end cycle
    print("\n[7. Disconnecting Services...]")
    broker.disconnect()
    
    print("\n==================================================")
    print("ACHELION ARMS - DAILY CYCLE COMPLETE")
    print("==================================================")
    append_to_log(SessionLogEntry(timestamp=datetime.now(timezone.utc).isoformat(), action_type='CYCLE_END', triggering_module='main', triggering_signal='Daily cycle complete.'), log_file)

