# Docker-Traffic-Capturer
Tool with which the HTTP traffic of a Docker network can be captured.

## Usage
When starting the application, [PyShark](https://kiminewt.github.io/pyshark/), a Python wrapper for [tshark](https://www.wireshark.org/docs/man-pages/tshark.html), is started to capture all HTTP packets in a given Docker bridge network.
The captured packets are stored locally and can be retrieved via the application's REST API.

To start the application, first build the Docker image with the following command.
```sh
docker build -t docker-traffic-capturer .
```

Now you can start the container you have just built with the following command to start capturing the packets.
Note that the container must be started in **network mode "host"**, otherwise it does not have access to the network interface.
The ID of the network to be monitored must be supplied as the environment variable `NETWORK_ID`.
```sh
docker run --net=host -e NETWORK_ID=$NETWORK_ID --rm docker-traffic-capturer
```

### How to obtain the Network ID?
To obtain the ID of the network you want to monitor, there are several options.

#### Using `docker inspect`
Using the `docker inspect` command, you can obtain the ID of a network, either by its name or by a specific container.

- Get the ID of the network that a container is part of:
```sh
docker inspect --format='{{range .NetworkSettings.Networks}}{{.NetworkID}}{{end}}' $CONTAINER_ID
```

*Example Output:*
```
53b735c32b9f09a8c2b1886098ad9a5438b1e073895b83d27a79d3c19942d13f
```

- Get the ID of a network by name
```sh
docker inspect --format='{{.Id}}' $NETWORK_NAME
```

*Example Output:*
```
1bb2f3f8d3bec043173cf860e408471acde07f67fc9a70bd14289184de504a13
```

#### Using `docker network ls`
Alternatively, you can also use `docker network ls` to display a list of all existing networks.
In the `ID` column, you will then find the network ID truncated to 12 characters, which you can also use for this application.
```sh
docker network ls
```

*Example Output:*
```
NETWORK ID     NAME                                                     DRIVER    SCOPE
1bb2f3f8d3be   custom_network                                           bridge    local
```

## Development
### Create a local virtual environment
[Virtual Python environments](https://docs.python.org/3/library/venv.html) can be created and managed using various tools.
In the following description, [Anaconda](https://docs.anaconda.com/) is used.

- Create a new virtual environment

```
conda create --force --name docker_traffic_capturer_env python=3.9
```

- Activate the newly-created environment

```
conda activate docker_traffic_capturer_env
```

- Install the dependencies listed in `requirements.txt`

```
pip install -r requirements.txt
```

- Use the environment in VS Code as the Python Interpreter by opening the command palette with `[CMD] + [SHIFT] + [P]`, typing in `Python: Select Interpreter` and choosing the environment you just created
