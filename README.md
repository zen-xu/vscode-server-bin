# vscode-server-bin
Due to the requirement of connecting to the internet to download specific dependencies for remote development in vscode, it can be inconvenient for users in an intranet environment where direct external access is not allowed.

However, this project can help bypass this issue if pip installation is allowed in the intranet.

# Download
Use pip to download:

```bash
# VSCODE_VERSION is the current version number of vscode, such as 1.71.2
python3 -m pip install vscode-server-bin==${VSCODE_VERSION}
```

# Installation

```bash
python3 -m vscode_server_bin
```

# License
This project is licensed under the Apache-2.0 License. See the [LICENSE](LICENSE) file for details.
