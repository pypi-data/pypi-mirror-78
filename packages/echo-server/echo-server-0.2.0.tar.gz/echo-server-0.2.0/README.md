# echo-server

Network service that send messages back to client. Used in network testing.

## Install

```shell
pip install echo-server
```

### Installed Commands

- echo-server

### Usage

```shell
C:\Users\test>echo-server --help
Usage: echo-server [OPTIONS] [PORT]...

  Start echo server on given ports. Press CTRL+C to stop. The default
  listenning port is 3682. You can listen on many ports at the same time.

  Example:

  echo-server 8001 8002 8003

Options:
  -i, --ignore-failed-ports
  -b, --binding TEXT         Default to 0.0.0.0.
  --help                     Show this message and exit.

```


## Releases

### v0.2.0 2020/09/03

- Add parameter binding, so that we can set the binding ip address.

### v0.1.3 2020/03/27

- Add ignore_failed_ports option.

### v0.1.2 2020/03/27

- Fix data print problem.

### v0.1.1 2020/03/27

- Fix port str typed problem.

### v0.1.0 2020/03/27

- First release