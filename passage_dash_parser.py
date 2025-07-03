# parser.py
import re
import pandas as pd
from datetime import datetime


def parse_log_lines(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    data = []
    passage_mapping = {}
    alarms = []

    for line in lines:
        line = line.strip()

        # Extract timestamp
        timestamp_match = re.match(r"\:\)\/(\d{8}\/\d{2}:\d{2}:\d{2}\.\d+)", line)
        timestamp = timestamp_match.group(1) if timestamp_match else None

        # TR Start
        if 'TR Start' in line:
            data.append({
                'timestamp': timestamp,
                'event': 'TR Start',
                'raw': line
            })

        # TR End
        elif 'TR End, TrT:' in line:
            usn_match = re.search(r'USN:([A-Z0-9]+)', line)
            result_match = re.search(r'Res:([A-Z0-9]+)', line)
            data.append({
                'timestamp': timestamp,
                'event': 'TR End',
                'USN': usn_match.group(1) if usn_match else None,
                'Result': result_match.group(1) if result_match else None,
                'raw': line
            })

        # Vehicle Passage Mapping
        elif 'Vehicle Id' in line and 'Passage Id' in line:
            v_match = re.search(r'Vehicle Id (\d+)', line)
            p_match = re.search(r'Passage Id (\d+)', line)
            if v_match and p_match:
                passage_mapping[v_match.group(1)] = p_match.group(1)

        # Alarm or Thresholds
        elif any(kw in line for kw in ['EV rate', 'Class mismatch', 'Unmatched tags']):
            alarms.append({
                'timestamp': timestamp,
                'alarm': line.split('/')[-2],
                'value': re.findall(r"\d+\.\d+", line),
                'raw': line
            })

    df_main = pd.DataFrame(data)
    df_map = pd.DataFrame([{'vehicle_id': k, 'passage_id': v} for k, v in passage_mapping.items()])
    df_alarms = pd.DataFrame(alarms)
    return df_main, df_map, df_alarms


if __name__ == '__main__':
    log_file = 'logs/TP01B-ALC-25052930.txt'
    df_main, df_map, df_alarms = parse_log_lines(log_file)
    df_main.to_csv('data/parsed_logs.csv', index=False)
    df_map.to_csv('data/vehicle_passage_map.csv', index=False)
    df_alarms.to_csv('data/alarm_thresholds.csv', index=False)
    print("✅ Parsed and saved.")
