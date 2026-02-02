# LARGE DATASET FOR HIGHER–LOWER GAME
# All values are on the SAME SCALE (followers in millions)
# Structure is intentionally simple for terminal games

DATASET = [
    {"name": "Instagram", "description": "Social media platform", "value": 650},
    {"name": "Cristiano Ronaldo", "description": "Footballer", "value": 610},
    {"name": "Lionel Messi", "description": "Footballer", "value": 490},
    {"name": "Selena Gomez", "description": "Singer & Actress", "value": 430},
    {"name": "Kylie Jenner", "description": "Reality TV & Businesswoman", "value": 400},
    {"name": "Dwayne Johnson", "description": "Actor & Wrestler", "value": 395},
    {"name": "Ariana Grande", "description": "Singer", "value": 380},
    {"name": "Kim Kardashian", "description": "Reality TV Star", "value": 360},
    {"name": "Beyoncé", "description": "Singer", "value": 320},
    {"name": "Khloé Kardashian", "description": "Reality TV Star", "value": 310},
    {"name": "Nike", "description": "Sportswear brand", "value": 305},
    {"name": "Justin Bieber", "description": "Singer", "value": 295},
    {"name": "Kendall Jenner", "description": "Model", "value": 290},
    {"name": "Taylor Swift", "description": "Singer-songwriter", "value": 280},
    {"name": "National Geographic", "description": "Media brand", "value": 275},
    {"name": "Virat Kohli", "description": "Cricketer", "value": 265},
    {"name": "Jennifer Lopez", "description": "Singer & Actress", "value": 250},
    {"name": "Nicki Minaj", "description": "Rapper", "value": 235},
    {"name": "Kourtney Kardashian", "description": "Reality TV Star", "value": 225},
    {"name": "Netflix", "description": "Streaming service", "value": 220},
    {"name": "Miley Cyrus", "description": "Singer & Actress", "value": 215},
    {"name": "Katy Perry", "description": "Singer", "value": 210},
    {"name": "Zendaya", "description": "Actress", "value": 200},
    {"name": "Shakira", "description": "Singer", "value": 195},
    {"name": "LeBron James", "description": "Basketball player", "value": 185},
    {"name": "Rihanna", "description": "Singer & Entrepreneur", "value": 180},
    {"name": "Ellen DeGeneres", "description": "TV host", "value": 175},
    {"name": "Drake", "description": "Rapper", "value": 170},
    {"name": "FC Barcelona", "description": "Football club", "value": 165},
    {"name": "Real Madrid", "description": "Football club", "value": 160},
    {"name": "Billie Eilish", "description": "Singer", "value": 155},
    {"name": "NASA", "description": "Space agency", "value": 150},
    {"name": "Emma Watson", "description": "Actress", "value": 145},
    {"name": "Chris Hemsworth", "description": "Actor", "value": 140},
    {"name": "Marvel Studios", "description": "Film studio", "value": 135},
    {"name": "Robert Downey Jr.", "description": "Actor", "value": 130},
    {"name": "Spotify", "description": "Music streaming service", "value": 125},
    {"name": "YouTube Music", "description": "Music platform", "value": 120},
    {"name": "Tom Holland", "description": "Actor", "value": 115},
    {"name": "Apple", "description": "Technology brand", "value": 110},
    {"name": "Samsung", "description": "Electronics brand", "value": 105},
    {"name": "Google", "description": "Technology company", "value": 100}
]

# NOTES FOR GAME DESIGN
# • Values are deliberately spread unevenly to create surprise
# • Mix of celebrities, brands, platforms increases intuition errors
# • Can easily extend by appending more dictionaries
# • Dataset size already supports long replayability
# • Works perfectly with random.choice()
