import uvicorn

from app import app
from app.core.logger import StandaloneApplication, StubbedGunicornLogger, config_logger
from app.core.config import settings

if __name__ == '__main__':
    config_logger()
    if settings.env.lower() == "development":
        uvicorn.run("app.main:app",
                    host=settings.host,
                    port=settings.port,
                    reload=True,
                    log_level=settings.log_level.lower())
    elif settings.env.lower() == "production":
        options = {
            "bind": "0.0.0.0",
            "workers": settings.workers,
            "accesslog": "-",
            "errorlog": "-",
            "worker_class": "uvicorn.workers.UvicornWorker",
            "logger_class": StubbedGunicornLogger
        }
        StandaloneApplication(app, options).run()
