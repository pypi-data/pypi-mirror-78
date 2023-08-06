[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![Open Source? Yes!](https://badgen.net/badge/Open%20Source%20%3F/Yes%21/blue?icon=github)](https://github.com/Naereen/badges/) ![PyTest](https://github.com/jeff-vincent/docker-lite-python/workflows/PyTest/badge.svg)




# docker-lite-python
A simple, Python-based Docker interface built on top of the [Docker SDK for Python](https://docker-py.readthedocs.io/en/stable/). 
Intended to programmatically spin up, pass communications to, and ultimately tear down single Docker containers.
Requires a local instance of Docker.

**[Installation](#installation)** | **[Quick Start](#quick-start)** | **[Reference](#reference)** | **[Examples](#examples)**

## Installation:
```
pip install docker-lite-python
```


## Quick Start:
```
$ sudo python3
>>>from docker_light_python import DockerLite
>>>dl = DockerLite()
```

start an Alpine container and keep it running
```
>>>dl.run_container('alpine:latest', 'alpine-container', 'sleep infinity')
```
exec into the running container
```
>>>dl.exec_into_running_container('alpine-container', 'echo "Hello World!"')
ExecResult(exit_code=0, output=b'Hello World!\n')
```
tear down that container!
```
>>>dl.kill_container('alpine-container')
0
```

## Reference:

| Methods | Args | Overview |
|---------|------|----------|
|`build_image()`|`*path_to_dir*: string: The path to the build directory.`|`Build a Docker image from a local Dockerfile.`|
||`*resulting_image_name*: string`|`Enforces best practice of explicitly naming images.`|
||||
|`list_containers()`|`*all*: bool: default=False`|`List running containers by default.`|
||||
|`run_container()`|`*image_name*: string`|`Run a Docker container, optionally with a command.`|
||`*resulting_container_name*: string`|`Enforces best practice of explicitly naming containers.`|
||`*command*: string: The command to run. `|`Optional.`|
||||
|`get_container_by_name()`|`*existing_container_name*: string`|`Get a Docker container by name.`|
||||
|`exec_into_running_container()`|`*existing_container_name*: string`|`Run a command in an active container.`|
||`*command*: string: The command to execute in the running Docker container.`|
||||
|`list_images()`|`None`|`List all images in the local Docker instance.`|
||||
|`remove_unused_images()`|`None`|`Equivalent of docker images prune`|
||||
|`remove_all_images()`|`None`|`Force removal of all images. Purge system.`|
||||
|`kill_container()`|`*existing_container_name*: string`|`Shut down and delete a container.`|
|||`NOTE: kill_container() technically just stops the containers, as they are self-removing.`|

## Examples:
```
from docker_lite import DockerLite

dl = DockerLite()
```
build image, 'my-image,' from a Dockerfile in the local directory

```
dl.build_image('./', 'my-image')
```

list all containers. Default is to list running containers

```
containers = dl.list_containers(all=True)
```

run a Docker container called 'my-container' based on a Docker image called 'my-image'

```
my_container = dl.run_container('my-image', 'my-container')
``` 

run a terminal command in a running Docker container called 'my-container'. Be creative

```
output = dl.exec_into_running_container('my-container', 'echo "Hello World!"')
```

get a container called 'my-container' by its unique name
```
container = dl.get_container('my-container')
``` 
 - [Python Docker SDK documentation on container objects here](https://docker-py.readthedocs.io/en/stable/containers.html#container-objects)

kill a container called 'my-container' by its unique name
```
dl.kill_container('my-container')
```
