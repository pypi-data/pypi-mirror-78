import docker

class DockerLite:

    def __init__(self):
        self.client = docker.from_env()

    def build_image(self, path_to_dir, resulting_image_name):
        """A method to build a Docker image from a Dockerfile. 
        Args:
            path_to_dockerfile: string: the path to the Dockerfile
            resulting_image_name: string: unique name for the image
        Returns:
            response: Python object: A given image. 
        """
        response = self.client.images.build(
                        path=path_to_dir,
                        tag=resulting_image_name)
        return response

    def list_containers(self, all=None):
        """A method for listing Docker containers. 
        Returns only running Docker containers by default.
        Args:
            all: bool: optional
        Returns:
            response: List: A list of container objects.
        """
        if all:
            response = self.client.containers.list(all=True)
        else:
            response = self.client.containers.list()
        return response

    def get_container_by_name(self, existing_container_name):
        """A method for getting a Python object that represents
        a given Docker container.
        Args:
            existing_container_name: string: the name of the Docker container
        Returns:
            response: Python object: a given Docker container
        """
        response = self.client.containers.get(existing_container_name)
        return response

    def run_container(self, image_name, resulting_container_name, command=None, volumes=None):
        """A method for running a Docker container. 
        Requires a name for the container.
        Args:
            image_name: string: the name of the Docker image to run
                        can be local or in Docker Hub.
            resulting_container_name: string: the name to set to the container
            command: string: the command to run at startup: optional
        Returns:
            response: Python object: the container being run.
        """
        response = self.client.containers.run(
                    image=image_name,  
                    name=resulting_container_name, 
                    command=command,
                    remove=True,
                    detach=True,
                    volumes=None)
        return response

    def exec_into_running_container(self, existing_container_name, command):
        container = self.get_container_by_name(existing_container_name)
        response = container.exec_run(command)
        return response

    def kill_container(self, existing_container_name):
        """A methond for stopping and removing a Docker container.
        Args:
            existing_container_name: string: the container to tear down
        Returns:
            0
        """
        container = self.get_container_by_name(existing_container_name)
        container.stop()
        return 0

    def list_images(self):
        """A method for listing all images on the system.
        Args:
            None
        Returns:
            image_list: List: a list of Python objects 
            representing all images on the system.
        """
        image_list = self.client.images.list()
        return image_list

    def remove_unused_images(self):
        """A method for removing unused images.
        Args:
            None
        Returns: 
            0
        """
        self.client.images.prune()
        return 0

    def remove_all_images(self):
        """A method for removing ALL images.
        Args:
            None
        Returns: 
            0
        """
        image_list = self.list_images()
        for image in image_list:
            self.client.images.remove(image.id, force=True)
        return 0
