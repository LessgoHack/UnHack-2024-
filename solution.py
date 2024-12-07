
import json
from collections import defaultdict

def parse(input_data):
    steps = {step["id"]: step for step in input_data["steps"]}
    machines = {machine["machine_id"]: machine for machine in input_data["machines"]}
    wafers = input_data["wafers"]
    return steps, machines, wafers

def parameters_in_range(params, ranges):
    return all(ranges[key][0] <= params[key] <= ranges[key][1] for key in params)

def schedule_wafers(steps, machines, wafers):
    schedule = []
    time = defaultdict(int)
    
    for wafer in wafers:
        for step_id in wafer["processing_times"]:
            step = steps[step_id]
            machines_for_step = [m for m in machines.values() if m["step_id"] == step_id]
            
            for i in range(wafer["quantity"]):
                wafer_id = f"{wafer['type']}-{i+1}"
                assigned = False
                
                for machine in machines_for_step:
                    machine_params = machine["initial_parameters"]
                    while not parameters_in_range(machine_params, step["parameters"]):
                        time[machine["machine_id"]] += machine["cooldown_time"]
                        machine_params = machine["initial_parameters"]
                    
                    start_time = time[machine["machine_id"]]
                    end_time = start_time + wafer["processing_times"][step_id]
                    schedule.append({
                        "wafer_id": wafer_id,
                        "step": step_id,
                        "machine": machine["machine_id"],
                        "start_time": start_time,
                        "end_time": end_time
                    })
                    time[machine["machine_id"]] = end_time
                    machine_params = {
                        key: machine_params[key] + machine["fluctuation"][key]
                        for key in machine_params
                    }
                    assigned = True
                    break
                
                if not assigned:
                    raise Exception(f"No machine available for wafer {wafer_id} at step {step_id}")
    
    return schedule


with open('Milestone0.json', 'r') as file:
    data = json.load(file)

steps, machines, wafers = parse(data)
schedule_plan = schedule_wafers(steps, machines, wafers)


for entry in schedule_plan:
    print(entry)
