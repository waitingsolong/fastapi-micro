class Role:
    DEFAULT = "football_fan"
    
    FOOTBALL_FAN = "football_fan"
    FOOTBALL_PLAYER = "football_player"
    ADMIN = "admin"
     
roles = {
    Role.FOOTBALL_FAN: ["read_articles"],
    Role.FOOTBALL_PLAYER: ["read_articles", "access_training"],
    Role.ADMIN: ["read_articles", "access_training", "manage_users"],
}
