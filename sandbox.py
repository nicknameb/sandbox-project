import docker
import time
import tarfile
import io
import subprocess
client = docker.from_env()

def ensure_image_exists(image_name):
    result = subprocess.run(["docker", "images", "-q", image_name], stdout=subprocess.PIPE, text=True)
    if not result.stdout.strip():
        print(f"Image '{image_name}' not found. building)")               #ensure the image is built before running
        subprocess.run(["docker", "build", "-t", image_name, "."]) 

def copy_to_container(container, file_path, container_path):
    tar_stream = io.BytesIO()
    with tarfile.TarFile(fileobj=tar_stream, mode='w') as tar:   #code to run and test an app in a container
        tar.add(file_path, arcname=container_path)
    tar_stream.seek(0)
    container.put_archive("/", tar_stream)
    print(f"Copied {file_path} to {container_path} in container.")

def run_sandbox_container(image_name, app_path):
    print(f"Running container from image: {image_name}")
    container = client.containers.run(
        image_name,                                           #define parameters
        detach=True,
        tty=True,
        nano_cpus=int(0.5 * 1e9),
        mem_limit="512m"
    )
    
    app_container_path = "/app/test_app"
    copy_to_container(container, app_path, app_container_path)
    
    # Execute the app inside the container
    execute_command_in_container(container, f"chmod +x {app_container_path}")
    execute_command_in_container(container, app_container_path) 
    execute_command_in_container(container, "clamscan /app/test_app")


    time.sleep(5)  
    print(f"Stopping container: {container.id}")
    container.stop()

def execute_command_in_container(container, command):
    exec_log = container.exec_run(command)

if __name__ == "__main__":
    app_to_test = "test_app.py"  
    ensure_image_exists("sandbox")
    run_sandbox_container("sandbox", app_to_test)
    
