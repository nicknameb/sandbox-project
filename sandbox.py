import docker
import time
import tarfile 
import io 

# Initialize Docker client
client = docker.from_env()

# Function to create and run a container
def run_sandbox_container(image_name):
    print(f"Running container from image: {image_name}")
    container = client.containers.run(
        image_name,
        detach=True,
        tty=True,
        nano_cpus= int(0.5 * 1e9),
        mem_limit="512m"
    ) 

    execute_command_in_container(container,"ps --help <s|l|o|t|m|a>" ) 
    #execute_command_in_container(container,"ls -la" ) 

    #print("Streaming logs:") 
    #for log in container.logs(stream=True):
        #print(log.decode().strip()) 

    time.sleep(5)  # Run for 5 seconds
    print(f"Stopping container: {container.id}")
    container.stop()

def execute_command_in_container(container, command):
    exec_log = container.exec_run(command)
    print(f"Command output: {exec_log.output.decode()}")

if __name__ == "__main__":
    run_sandbox_container("sandbox")
    