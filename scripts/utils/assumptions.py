# Assumptions and AFCON System
GD_factor = 0.25
win_factor = 1.0
draw_factor = 0.5

# Weight of tournaments and stages
tournament_weight = {
    "African Cup of Nations": 2.0,
    "FIFA World Cup qualification": 2.0,
    "African Cup of Nations qualification": 1.5}

stage_weight = {
    "Group Stage": 1.0,
    "Round of 16": 1.5,
    "Quarter final": 1.75,
    "Semi final": 2.0,
    "Third Place": 1.75,
    "Final": 2.25}

# AFCON Tournament system through the years 
stages_2019_2027 = [("Final", 1), ("Third Place", 1), ("Semi final", 2), ("Quarter final", 4), ("Round of 16", 8),]
stages_1992_2019 = [("Final", 1), ("Third Place", 1), ("Semi final", 2), ("Quarter final", 4),]
stages_1978_1992 = [("Final", 1), ("Third Place", 1), ("Semi final", 2),]
stages_1968_1978 = [("Final", 1), ("Third Place", 1), ("Semi final", 2),]
stages_1963_1968 = [("Final", 1), ("Third Place", 1),]
stages_1976 = [("Final Group", 4),] 

