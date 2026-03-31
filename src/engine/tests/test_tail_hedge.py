"""
Unit tests for the PTRH Full Automation module (tail_hedge.py).
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import datetime

# Add the engine directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tail_hedge import OptionsPosition, run_ptrh_module
from cam import CamInputs

class TestPTRHAutomation(unittest.TestCase):
    """
    Test suite for the run_ptrh_module function.
    We use mocking to simulate execution calls and isolate the logic.
    """

    @patch('tail_hedge.execute_notional_correction')
    @patch('tail_hedge.execute_roll')
    def test_clean_run_no_action(self, mock_execute_roll, mock_execute_correction):
        """Tests a scenario where the hedge is correctly sized and no roll is needed."""
        cam_inputs = CamInputs(
            current_equity_pct=0.75, regime_score=0.55, fem_concentration_score=0.5,
            macro_stress_score=0.4, cdm_active_signals=0, nav=50_000_000
        )
        # CAM will require ~1.5% NAV = $750k. Actual is $750k.
        positions = [
            OptionsPosition('QQQ', 'PUT', 450.0, (datetime.date.today() + datetime.timedelta(days=90)).isoformat(), 100, 750_000)
        ]
        status = run_ptrh_module(cam_inputs, positions)
        
        self.assertEqual(status.last_action, "NONE")
        mock_execute_roll.assert_not_called()
        mock_execute_correction.assert_not_called()

    @patch('tail_hedge.execute_notional_correction')
    @patch('tail_hedge.execute_roll')
    def test_dte_roll_trigger(self, mock_execute_roll, mock_execute_correction):
        """Tests that a DTE of <= 30 triggers a roll."""
        cam_inputs = CamInputs(
            current_equity_pct=0.75, regime_score=0.55, fem_concentration_score=0.5,
            macro_stress_score=0.4, cdm_active_signals=0, nav=50_000_000
        )
        positions = [
            OptionsPosition('QQQ', 'PUT', 450.0, (datetime.date.today() + datetime.timedelta(days=29)).isoformat(), 100, 750_000)
        ]
        status = run_ptrh_module(cam_inputs, positions)

        self.assertEqual(status.last_action, "ROLL")
        mock_execute_roll.assert_called_once()
        mock_execute_correction.assert_not_called()

    @patch('tail_hedge.execute_notional_correction')
    @patch('tail_hedge.execute_roll')
    def test_under_hedged_correction(self, mock_execute_roll, mock_execute_correction):
        """Tests that a significant under-hedge triggers a correction."""
        cam_inputs = CamInputs(
            current_equity_pct=0.75, regime_score=0.55, fem_concentration_score=0.5,
            macro_stress_score=0.4, cdm_active_signals=0, nav=50_000_000
        )
        # CAM requires $750k. Actual is $600k. Drift = -20% (< -5%).
        positions = [
            OptionsPosition('QQQ', 'PUT', 450.0, (datetime.date.today() + datetime.timedelta(days=90)).isoformat(), 80, 600_000)
        ]
        status = run_ptrh_module(cam_inputs, positions)

        self.assertEqual(status.last_action, "CORRECT_DRIFT")
        mock_execute_roll.assert_not_called()
        mock_execute_correction.assert_called_once()
        # Check that it's buying (positive delta)
        self.assertGreater(mock_execute_correction.call_args[0][0], 0)

    @patch('tail_hedge.execute_notional_correction')
    @patch('tail_hedge.execute_roll')
    def test_over_hedged_outside_tolerance(self, mock_execute_roll, mock_execute_correction):
        """Tests that a significant over-hedge (>15%) triggers a correction."""
        cam_inputs = CamInputs(
            current_equity_pct=0.75, regime_score=0.55, fem_concentration_score=0.5,
            macro_stress_score=0.4, cdm_active_signals=0, nav=50_000_000
        )
        # CAM requires $750k. Actual is $900k. Drift = +20% (> 15%).
        positions = [
            OptionsPosition('QQQ', 'PUT', 450.0, (datetime.date.today() + datetime.timedelta(days=90)).isoformat(), 120, 900_000)
        ]
        status = run_ptrh_module(cam_inputs, positions)

        self.assertEqual(status.last_action, "CORRECT_DRIFT")
        mock_execute_roll.assert_not_called()
        mock_execute_correction.assert_called_once()
        # Check that it's selling (negative delta)
        self.assertLess(mock_execute_correction.call_args[0][0], 0)
        
    @patch('tail_hedge.execute_notional_correction')
    @patch('tail_hedge.execute_roll')
    def test_over_hedged_inside_tolerance(self, mock_execute_roll, mock_execute_correction):
        """Tests that a minor over-hedge (<15%) is tolerated."""
        cam_inputs = CamInputs(
            current_equity_pct=0.75, regime_score=0.55, fem_concentration_score=0.5,
            macro_stress_score=0.4, cdm_active_signals=0, nav=50_000_000
        )
        # CAM requires $750k. Actual is $825k. Drift = +10% (< 15%).
        positions = [
            OptionsPosition('QQQ', 'PUT', 450.0, (datetime.date.today() + datetime.timedelta(days=90)).isoformat(), 110, 825_000)
        ]
        status = run_ptrh_module(cam_inputs, positions)

        self.assertEqual(status.last_action, "NONE")
        mock_execute_roll.assert_not_called()
        mock_execute_correction.assert_not_called()

if __name__ == '__main__':
    unittest.main()
