import json

def save_highscore(cash, point):
    try:
        with open("highscores.json", "r", encoding="utf-8") as file:
            highscore = json.load(file)
    
    except FileNotFoundError:
        highscore = []
        return "chicken"
    
    except Exception as e:
        return (f"Smth got fricked! Error: {e}")
    
    
    highscore.append({"score": point, "cash": cash})
    print(highscore)
    
    try:
        with open("highscores.json", "w", encoding="utf-8") as file:
            json.dump(highscore, file, indent=4)
    except Exception as e:
        return (f"Smth got fricked! Error: {e}")
        
print(save_highscore(20000, 12))

