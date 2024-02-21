from __future__ import annotations

from typing import Optional, Union
import subprocess
import sys
import json
import secrets
import socket
import atexit


from .base import JupyterConnectable, JupyterConnectionInfo
from .jupyter_client import JupyterClient


def _get_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]


class LocalJupyterServer(JupyterConnectable):
    class GenerateToken:
        pass

    def __init__(
        self,
        ip: str = "127.0.0.1",
        port: Optional[int] = None,
        token: Union[str, GenerateToken] = GenerateToken(),
        log_file: str = "jupyter_gateway_{port}.log",
        log_level="DEBUG",
        log_max_bytes=1048576,
        log_backup_count=3,
    ):
        # Check Jupyter gateway server is installed
        try:
            subprocess.run(
                [sys.executable, "-m", "jupyter", "kernelgateway", "--version"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
        except subprocess.CalledProcessError:
            raise ValueError(
                "Jupyter gateway server is not installed. Please install it with `pip install jupyter_kernel_gateway`."
            )

        self.ip = ip
        if port is None:
            port = _get_free_port()
        self.port = port

        if isinstance(token, LocalJupyterServer.GenerateToken) or token is LocalJupyterServer.GenerateToken:
            token = secrets.token_urlsafe(32)

        self.token = token
        log_file = log_file.replace("{port}", str(port))

        logging_config = {
            "handlers": {
                "file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "level": log_level,
                    "maxBytes": log_max_bytes,
                    "backupCount": log_backup_count,
                    "filename": log_file,
                    "mode": "w",
                }
            },
            "loggers": {"KernelGatewayApp": {"level": log_level, "handlers": ["file", "console"]}},
        }

        # Run Jupyter gateway server with detached subprocess
        args = [
            sys.executable,
            "-m",
            "jupyter",
            "kernelgateway",
            "--KernelGatewayApp.ip",
            ip,
            "--KernelGatewayApp.port",
            str(port),
            "--KernelGatewayApp.auth_token",
            token,
            "--JupyterApp.answer_yes",
            "true",
            "--JupyterApp.logging_config",
            json.dumps(logging_config),
            "--JupyterWebsocketPersonality.list_kernels",
            "true",
        ]
        self._subprocess = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Read stderr until we see "is available at" or the process has exited with an error
        while True:
            result = self._subprocess.poll()
            if result is not None:
                raise ValueError(
                    f"Jupyter gateway server failed to start. Please check the logs ({log_file}) for more information."
                )
            line = self._subprocess.stderr.readline()
            if "is available at" in line:
                break

        # Poll the subprocess to check if it is still running
        result = self._subprocess.poll()
        if result is not None:
            raise ValueError(
                f"Jupyter gateway server failed to start. Please check the logs ({log_file}) for more information."
            )

        atexit.register(self.stop)

    def stop(self):
        if self._subprocess.poll() is None:
            self._subprocess.send_signal(subprocess.signal.SIGINT)
            self._subprocess.wait()

    @property
    def connection_info(self) -> JupyterConnectionInfo:
        return JupyterConnectionInfo(host=self.ip, use_https=False, port=self.port, token=self.token)

    def get_client(self) -> JupyterClient:
        return JupyterClient(self.connection_info)

    def __enter__(self) -> LocalJupyterServer:
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()
