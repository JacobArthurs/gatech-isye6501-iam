import simpy
import random
import numpy as np

# Passenger arrival rate (per minute)
ARRIVAL_RATE = 5
# Mean service time for ID check
SERVICE_RATE = 0.75
# Minimum time for personal scanner
PERSONAL_SCAN_TIME_MIN = 0.5
# Maximum time for personal scanner
PERSONAL_SCAN_TIME_MAX = 1.0
# Simulation time (minutes)
SIM_TIME = 1000
# Maximum wait time
MAX_WAIT_TIME = 15

# Function to simulate the airport security process
def passenger(env, id_checkers, personal_check_queues, wait_times):
    arrival_time = env.now

    # ID check process
    with id_checkers.request() as req:
        yield req
        yield env.timeout(random.expovariate(1 / SERVICE_RATE))

    # Choose the shortest personal-check queue
    shortest_queue = min(personal_check_queues, key=lambda q: len(q.queue))
    with shortest_queue.request() as req:
        yield req
        yield env.timeout(random.uniform(PERSONAL_SCAN_TIME_MIN, PERSONAL_SCAN_TIME_MAX))

    # Calculate total wait time
    wait_times.append(env.now - arrival_time)

# Passenger arrival process
def passenger_arrivals(env, id_checkers, personal_check_queues, wait_times):
    while True:
        yield env.timeout(random.expovariate(ARRIVAL_RATE))
        env.process(passenger(env, id_checkers, personal_check_queues, wait_times))

# Function to run the simulation
def run_simulation(id_checker_count, personal_queue_count):
    env = simpy.Environment()
    id_checkers = simpy.Resource(env, capacity=id_checker_count)
    personal_check_queues = [simpy.Resource(env, capacity=1) for _ in range(personal_queue_count)]
    wait_times = []

    env.process(passenger_arrivals(env, id_checkers, personal_check_queues, wait_times))
    env.run(until=SIM_TIME)

    return np.mean(wait_times)

# Function to determine optimal and minimum configuration
def find_optimal():
    optimal_config = None
    minimum_config = None

    for id_checkers in range(1, 11):
        for personal_queues in range(1, 11):
            avg_wait_time = run_simulation(id_checkers, personal_queues)
            print(f"{'Pass:' if avg_wait_time < MAX_WAIT_TIME else 'Fail:'} {id_checkers} ID checkers, {personal_queues} personal queues -> Avg wait: {avg_wait_time:.2f} min")
            if avg_wait_time < MAX_WAIT_TIME:
                if optimal_config is None or avg_wait_time < optimal_config[2]:
                    optimal_config = (id_checkers, personal_queues, avg_wait_time)
                
                if minimum_config is None or (id_checkers + personal_queues) < (minimum_config[0] + minimum_config[1]):
                    minimum_config = (id_checkers, personal_queues, avg_wait_time)

    return optimal_config, minimum_config

# Run and print results
optimal, minimum = find_optimal()
print(f"Optimal: {optimal[0]} ID checkers, {optimal[1]} personal queues -> Avg wait: {optimal[2]:.2f} min")
print(f"Minimum: {minimum[0]} ID checkers, {minimum[1]} personal queues -> Avg wait: {minimum[2]:.2f} min")
