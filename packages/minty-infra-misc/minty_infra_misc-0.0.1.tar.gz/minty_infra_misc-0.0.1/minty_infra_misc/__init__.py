# SPDX-FileCopyrightText: Mintlab B.V.
#
# SPDX-License-Identifier: EUPL-1.2


from minty import Base
from redis import Redis

__version__ = "0.0.1"


class RedisInfrastructure(Base):
    def __init__(self):
        "Initialize a new Redis infrastructure factory"
        self.name = "session"

    def __call__(self, config: dict):
        "Create a new Redis connection from the specified configuration"
        redis_config = config["redis"][self.name]
        return Redis(**redis_config)
