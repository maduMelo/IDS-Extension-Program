import can, csv

filename = 'can_log.csv'
with open(filename, mode='w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    
    header = ['Timestamp', 'Arbitration ID', 'Extended ID', 'RTR', 'DLC'] + [f'B{i}' for i in range(1,9)]
    csv_writer.writerow(header)


with can.Bus(interface='socketcan', channel='can0', bitrate=500000) as bus:
    for msg in bus:
        with open(filename, mode='a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            row = [
                msg.timestamp,
                msg.arbitration_id,
                msg.is_extended_id,
                msg.is_remote_frame,
                msg.dlc
            ]
            row += list(msg.data) + [None] * (8 - len(msg.data))
            csv_writer.writerow(row)