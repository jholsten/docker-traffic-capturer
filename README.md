# Docker-Traffic-Capturer
Tool with which the HTTP traffic of a Docker network can be captured.

## Usage
When starting the application, [PyShark](https://kiminewt.github.io/pyshark/), a Python wrapper for [tshark](https://www.wireshark.org/docs/man-pages/tshark.html), is started to capture all HTTP packets in a given Docker bridge network.
The captured packets are stored locally and can be retrieved via the application's REST API.

The application is available as a Docker image 
```
gitlab.informatik.uni-bremen.de:5005/jholsten/docker-traffic-capturer:latest
```
in the [Container Registry](https://gitlab.informatik.uni-bremen.de/jholsten/docker-traffic-capturer/container_registry).
Alternatively, you can also build the image from source.
```sh
docker build -t docker-traffic-capturer .
```

Now you can start the container with the following command to start capturing the packets.
Note that the container must be started in **network mode "host"**, otherwise it does not have access to the network interface.
The ID of the network to be monitored must be supplied as the environment variable `NETWORK_ID`.
```sh
docker run --net=host -e NETWORK_ID=$NETWORK_ID --rm docker-traffic-capturer
```

With this command, the REST API is started by default on a randomly selected available port in order to be able to run multiple containers simultaneously in the host's network.
The selected port is then stored in a file named `API_PORT` in the working directory `/app`.
As an alternative to the random selection of a port, the port can also be specified via an environment variable named `FIXED_API_PORT`.

### Retrieving the collected Packets
The captured packets can be retrieved via two different API endpoints:
- `GET /collect` - Returns the collected packets as a JSON array.
- `POST /collect/file/$filename` - Stores the collected packets in a file named `filename`.

Note that calling one of these two endpoints causes the internal memory to be reset.
The next time any of these endpoints is called, only the new packets captured afterwards will be available.

#### Retrieving the collected Packets on MacOS and Windows
Since publishing a port in network mode "host" is only supported on Linux, but not on Windows or MacOS, the API cannot be accessed by such hosts (see [Docker Documentation](https://docs.docker.com/network/drivers/host/)).
Therefore, the bash scripts `collect.sh` and `collect_to_file.sh` offer an alternative with which the endpoints `GET /collect` and `POST /collect/file/$filename` can be called from inside the container.

##### `collect.sh`
By executing `collect.sh`, the packets collected so far can be retrieved.
The script calls the endpoint `GET /collect` and outputs the result to STDOUT.
To execute the script from outside the container, use the `docker exec` command.

```sh
docker exec $CONTAINER_ID sh -c "sh collect.sh"
```

##### `collect_to_file.sh`
Executing the bash script `collect_to_file.sh` allows to store the collected packets in a given file.
The name of the file to which the packets are to be written needs to be supplied via the parameter `-f`.
Therefore, the bash script `collect_to_file.sh` offers an alternative with which the endpoint `POST /collect/file/$filename` can be called in order to store the collected packets in a file.
This script can be executed within the container using the `docker exec` command and passing the name of the file to which the packets are to be written via the parameter `-f`.

```sh
docker exec $CONTAINER_ID sh -c "sh collect_to_file.sh -f $filename"
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

```sh
conda create --force --name docker_traffic_capturer_env python=3.9
```

- Activate the newly-created environment

```sh
conda activate docker_traffic_capturer_env
```

- Install the dependencies listed in `requirements.txt`

```sh
pip install -r requirements.txt
```

- Use the environment in VS Code as the Python Interpreter by opening the command palette with `[CMD] + [SHIFT] + [P]`, typing in `Python: Select Interpreter` and choosing the environment you just created
