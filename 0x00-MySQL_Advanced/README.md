0x00-MySQL_Advanced

## Table Of Contents

- [Table Of Contents](#table-of-contents)
- [Running MySQL 5.7 in docker container(Using Vscode)](#running-mysql-57-in-docker-containerusing-vscode)
  - [Helpful resources](#helpful-resources)
  - [References](#references)

## Running MySQL 5.7 in docker container(Using Vscode)

```bash
docker run --name alxsql -d \
    -p 3308:3308 \
    -e MYSQL_ROOT_PASSWORD=alxpwd \
    -v alxsql:/var/lib/mysql \
    mysql:5.7

```

- `docker run`: This is the command to create and run a new Docker container.
- `--name alxsql`: This specifies the name of the container as "mysql".
- `-d`: This option tells Docker to run the container in detached mode, so it runs in the background.
- `-p 3306:3306`: This maps port 3306 from the host to port 3306 inside the container, allowing you to access MySQL from the host machine.
- `-e MYSQL_ROOT_PASSWORD=alxpwd`: This sets the environment variable `MYSQL_ROOT_PASSWORD` in the container, providing the root password for MySQL. You should replace "alxpwd" with a more secure password.
- `-v mysql:/var/lib/mysql`: This creates a Docker volume named "mysql" and mounts it to the `/var/lib/mysql` directory inside the container.
- `mysql:5.7`: This specifies the Docker image to use, telling Docker to pull the official MySQL version 8 image from the Docker Hub and use it to start the container.

### Helpful resources

- [How to install docker on Windows](https://www.geeksforgeeks.org/how-to-install-docker-on-windows/)

- [How to install and use docker on ubuntu](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04)

  > Note: You don't have to go through the entire content here. For now, you can just install docker and move on if u want.

- [Docker refused to run?](https://docs.docker.com/engine/install/linux-postinstall/)

  > The above article contains guidelines you must follow right after installing docker for the first time on linux

- [How to install docker extension for vscode](https://code.visualstudio.com/docs/containers/overview)

### References

- [How to Use Docker for Your MySQL Database ](https://earthly.dev/blog/docker-mysql/)
- [Official Docker mysql guide](https://hub.docker.com/_/mysql)
