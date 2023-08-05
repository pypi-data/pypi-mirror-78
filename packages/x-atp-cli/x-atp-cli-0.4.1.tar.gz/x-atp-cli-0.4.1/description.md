## X-ATP CLI Client

X automated test platform command line client.

```shell
usage: x-atp-cli [-h] [-v] [-d] [-r ATP_SERVER_URL] [-t TEST_TYPE]
                 [-n WORKSPACE_NAME]

X ATP CLI Client (X automated test platform command line client)

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         Output client version information
  -d, --demo            Create x_sweetest_example project in the current
                        directory
  -r ATP_SERVER_URL, --run ATP_SERVER_URL
                        Run X-ATP automated test execution side service (E.g x-atp-cli -r http://127.0.0.1
                        -t api)
  -t TEST_TYPE, --type TEST_TYPE
                        Client Run test Type api|web (used with parameter -r)
  -n WORKSPACE_NAME, --name WORKSPACE_NAME
                        The identifier name of the execution workspace (used with parameter -r)
```
