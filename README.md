# Docker-Traffic-Capturer
Tool with which the HTTP traffic of a Docker network can be monitored.

## Usage
```
docker build -t docker-traffic-capturer .
docker run --net=host -e NETWORK_ID=$NETWORK_ID --rm docker-traffic-capturer
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
