import subprocess
import time

journalctl_cmd = "sudo journalctl -u stationd -f --no-hostname -o cat"

error_keywords = ["VerifyPod transaction Error=\"rpc error: code = Unknown desc = rpc error: code = Unknown"]

command_to_run = "sudo systemctl stop stationd && cd tracks && git pull && go run cmd/main.go rollback && go run cmd/main.go rollback && go run cmd/main.go rollback && sudo systemctl restart stationd && sudo journalctl -u stationd -f --no-hostname -o cat"

def run_command(command):
    subprocess.run(command, shell=True)

def monitor_log():
    process = subprocess.Popen(journalctl_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    while True:
        output = process.stdout.readline()
        if output == b'' and process.poll() is not None:
            break
        if output:
            line = output.strip().decode()
            print(line)
            for error_keyword in error_keywords:
                if error_keyword in line:
                    run_command(command_to_run)
                    print(f"Command '{command_to_run}' executed due to error '{error_keyword}' in log.")
                    break 
        time.sleep(1)

if __name__ == "__main__":
    monitor_log()
