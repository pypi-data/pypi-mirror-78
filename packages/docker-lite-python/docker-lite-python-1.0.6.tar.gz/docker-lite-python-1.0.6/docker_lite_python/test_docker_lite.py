import os
import docker
from docker_lite_python.docker_lite import DockerLite

dl = DockerLite()
CONTAINER_NAME = 'test-container'

def test_run_container():
    container = dl.run_container(
                image_name='alpine',
                resulting_container_name=CONTAINER_NAME)
    assert container.name == CONTAINER_NAME
    container.stop()

def test_exec_into_running_container():
    container = dl.run_container(
                image_name='alpine',
                command='sleep infinity',
                resulting_container_name=CONTAINER_NAME)
    response = dl.exec_into_running_container(container.name, 'echo "Hello World!"')
    assert "output=b'Hello World!\\n'" in str(response)

def test_get_container_by_name():
    container = dl.get_container_by_name(CONTAINER_NAME)
    assert container.name == CONTAINER_NAME

def test_list_containers():
    response = dl.list_containers(all=True)
    container = response[0]
    assert CONTAINER_NAME in container.name
    container.stop()

def test_remove_images():
    response = dl.remove_all_images()
    image_list = dl.list_images()
    assert response == 0 and image_list == []

def test_build_image():
    with open('Dockerfile', 'w+') as dockerfile:
        dockerfile.write('FROM alpine:latest')
    image = dl.build_image('./', 'alpine')
    assert type(image) == tuple
    os.remove('Dockerfile')
    dl.remove_all_images()
