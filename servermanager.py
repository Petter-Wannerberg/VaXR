import docker
import time
import random
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Back4App API credentials
B4A_APP_ID = os.environ.get('B4A_APP_ID')
B4A_REST_API_KEY = os.environ.get('B4A_REST_API_KEY')

B4A_API_URL = 'https://parseapi.back4app.com'

INTERVAL = 5

client = docker.from_env()

def get_active_lessons():
    headers = {
        'X-Parse-Application-Id': B4A_APP_ID,
        'X-Parse-REST-API-Key': B4A_REST_API_KEY
    }
    params = {
    #    'where': '{"status":"active"}',
    #    'order': 'createdAt'
    }
    response = requests.get(f'{B4A_API_URL}/classes/Lesson', headers=headers, params=params)
    response.raise_for_status()
    return response.json().get('results', [])

def update_lesson_info(lesson_id, host_port):
    headers = {
        'X-Parse-Application-Id': B4A_APP_ID,
        'X-Parse-REST-API-Key': B4A_REST_API_KEY,
        'Content-Type': 'application/json'
    }
    data = {
        'port': int(host_port)  # Ensure host_port is an integer
    }
    try:
        response = requests.put(f'{B4A_API_URL}/classes/Lesson/{lesson_id}', headers=headers, json=data)
        response.raise_for_status()
        print(f"Successfully updated lesson {lesson_id} with port {host_port}")
    except requests.exceptions.RequestException as e:
        print(f"Error updating lesson {lesson_id}: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response content: {e.response.content}")
        raise

def find_free_port():
    while True:
        port = random.randint(10000, 65535)
        if not client.containers.list(filters={'publish': port}):
            return port

def start_container(lesson_code):
    image_name = 'git.ri.se:4567/teknologier-for-interaktion/vaxr-lab'
    host_port = find_free_port()

    try:
        # Pull the latest version of the image
        client.images.pull(image_name)
        print(f"Successfully pulled latest version of {image_name}")
    except docker.errors.APIError as e:
        print(f"Error pulling image {image_name}: {e}")
        # If pull fails, we'll continue with the existing image

    try:
        container = client.containers.run(
                        image_name,
                        name=f'vaxr-server-{lesson_code}',
                        detach=True,
                        ports={'7777/udp': host_port},
                        command=f'-LessonCode={lesson_code}'
                )
        return container, host_port
    except docker.errors.APIError as e:
        print(f"Error starting container for lesson {lesson_code}: {e}")
        raise

def stop_container(container_name):
    try:
        container = client.containers.get(container_name)
        container.stop()
        container.remove()
        print(f"Stopped and removed container: {container_name}")
    except docker.errors.NotFound:
        print(f"Container not found: {container_name}")

def main():
    while True:
        try:
            active_lessons = get_active_lessons()
            active_lesson_codes = set(lesson.get('code') for lesson in active_lessons)

            # Start or update containers for active lessons
            for lesson in active_lessons:
                lesson_code = lesson.get('code')
                lesson_id = lesson.get('objectId')
                existing_containers = client.containers.list(filters={'name': f'vaxr-server-{lesson_code}'})
                if not existing_containers:
                    container, host_port = start_container(lesson_code)
                    update_lesson_info(lesson_id, host_port)
                else:
                    # Container exists, make sure we have the port info
                    container = existing_containers[0]
                    host_port = container.attrs['NetworkSettings']['Ports']['7777/udp'][0]['HostPort']
                    if lesson.get('port') != int(host_port):
                        update_lesson_info(lesson_id, host_port)

            # Stop containers for inactive lessons
            all_containers = client.containers.list(all=True)
            for container in all_containers:
                if container.name.startswith('vaxr-server-'):
                    lesson_code = container.name[len('vaxr-server-'):]
                    if lesson_code not in active_lesson_codes:
                        stop_container(container.name)

            time.sleep(INTERVAL)  # Check every minute
        except requests.exceptions.RequestException as e:
            print(f"Error communicating with Back4App: {e}")
            time.sleep(INTERVAL)  # Wait before retrying
        except docker.errors.DockerException as e:
            print(f"Error with Docker operations: {e}")
            time.sleep(INTERVAL)  # Wait before retrying

if __name__ == "__main__":
    main()