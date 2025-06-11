import csv
from database.models import SessionLocal, User

def export_stats_to_csv(filepath):
    db = SessionLocal()
    users = db.query(User).all()
    db.close()

    try:
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['username', 'games_played', 'games_won']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for user in users:
                writer.writerow({
                    'username': user.username,
                    'games_played': user.games_played,
                    'games_won': user.games_won
                })
        return True, f"Dane wyeksportowano do {filepath}"
    except Exception as e:
        return False, f"Błąd podczas eksportu: {e}"