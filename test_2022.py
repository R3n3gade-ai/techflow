from src.simulation.historical_engine import run_simulation
from src.simulation.tearsheet import generate_tearsheet
res = run_simulation("2022-01-01", "2022-12-31")
generate_tearsheet(res.history, "2022-01-01", "2022-12-31", 50000000.0)
