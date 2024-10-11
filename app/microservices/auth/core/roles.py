from enum import Enum

class Role(str, Enum):
    football_fan = "football_fan"
    football_player = "football_player"
    admin = "admin"
     
roles = {
    Role.football_fan: ["read_articles"],
    Role.football_player: ["read_articles", "access_training"],
    Role.admin: ["read_articles", "access_training", "manage_users"],
}

DEFAULT_ROLE = Role.football_fan
