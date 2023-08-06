from flask_limiter import Limiter
from flask import Flask
from typing import Any, Union
from limits.errors import ConfigurationError


class RedisLimiter(Limiter):
    """
    Class extends Flask-Limiter with Redis-specific configuration and automatic checks
    """

    logger: Any = None

    def __init__(
        self,
        *args: Union[None, str, dict, list, Flask],
        **kwargs: Union[None, str, dict, list, Flask],
    ) -> None:
        """
        Patch in any Flask log handlers before firing up to parent for limiter initialization
        :param app: A configured Flask application object
        :return: None
        :raise ConfigurationError: if Redis is incorrectly configured (via self.init_app -> invoked through superclass)
        """
        app = kwargs.get("app")
        if app:
            self.logger = app.logger
            for handler in app.logger.handlers:
                self.logger.debug(f"Adding log handler to limiter: {handler}")
                self.logger.addHandler(handler)

        super().__init__(*args, **kwargs)

    def init_app(self, app: Flask) -> None:
        """
        patch self._check_storage into Flask-limiter
        :param app: Configured Flask app to use for rate limiting
        :return: None
        :raise ConfigurationError: if Redis is incorrectly configured
        """
        super().init_app(app=app)
        self._check_storage()

    def _check_storage(self) -> None:
        """
        Check the Redis storage backed is connected correctly
        :return: None
        :raise ConfigurationError: if Redis is incorrectly configured
        """
        if not self._storage.check():
            self.logger.critical(f"Invalid Redis configuration: {self._storage_uri}")
            raise ConfigurationError("Invalid Redis configuration")
