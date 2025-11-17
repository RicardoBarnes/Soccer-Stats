import requests
import pandas as pd
import matplotlib.pyplot as plt

# Your Football Data API key
API_KEY = ''
TEAM_IDS = [64, 68]  # Example: Liverpool FC and Manchester City
TEAM_NAMES = ["Liverpool FC", "Manchester City"]  # Names of the teams
SEASON = '2023'  # Specify the season

def fetch_team_data(team_id):
    url = f'https://api.football-data.org/v4/teams/{team_id}/matches?season={SEASON}'
    headers = {'X-Auth-Token': API_KEY}
    response = requests.get(url, headers=headers)
    matches = response.json()['matches']
    
    data = {
        "Date": [match['utcDate'][:10] for match in matches],
        "Opponent": [match['awayTeam']['name'] if match['homeTeam']['id'] == team_id else match['homeTeam']['name'] for match in matches],
        "Goals Scored": [match['score']['fullTime']['home'] if match['homeTeam']['id'] == team_id else match['score']['fullTime']['away'] for match in matches],
        "Goals Conceded": [match['score']['fullTime']['away'] if match['homeTeam']['id'] == team_id else match['score']['fullTime']['home'] for match in matches],
        "Result": [
            "Win" if (match['score']['winner'] == 'HOME_TEAM' and match['homeTeam']['id'] == team_id) or 
                     (match['score']['winner'] == 'AWAY_TEAM' and match['awayTeam']['id'] == team_id)
            else "Loss" if match['score']['winner'] else "Draw"
            for match in matches
        ]
    }
    
    return pd.DataFrame(data)

def analyze_team(df):
    total_goals_scored = df["Goals Scored"].sum()
    total_goals_conceded = df["Goals Conceded"].sum()
    wins = df[df["Result"] == "Win"].count()["Result"]
    losses = df[df["Result"] == "Loss"].count()["Result"]
    draws = df[df["Result"] == "Draw"].count()["Result"]
    win_loss_ratio = wins / losses if losses > 0 else float('inf')
    
    return total_goals_scored, total_goals_conceded, wins, losses, draws, win_loss_ratio

def display_team_stats(team_name, metrics):
    print(f"\n{team_name} Statistics:")
    print(f"Total Goals Scored: {metrics[0]}")
    print(f"Total Goals Conceded: {metrics[1]}")
    print(f"Wins: {metrics[2]}")
    print(f"Losses: {metrics[3]}")
    print(f"Draws: {metrics[4]}")
    print(f"Win/Loss Ratio: {metrics[5]:.2f}")

# Fetch data for both teams
df_team1 = fetch_team_data(TEAM_IDS[0])
df_team2 = fetch_team_data(TEAM_IDS[1])

# Analyze data for both teams
metrics_team1 = analyze_team(df_team1)
metrics_team2 = analyze_team(df_team2)

# Display team statistics
display_team_stats(TEAM_NAMES[0], metrics_team1)
display_team_stats(TEAM_NAMES[1], metrics_team2)

# Bar chart for goals scored vs. goals conceded 
plt.figure(figsize=(14, 7))
bar_width = 0.35
index = range(2)

bar1 = plt.bar([i - bar_width / 2 for i in index], [metrics_team1[0], metrics_team2[0]], bar_width, label='Goals Scored', color='green')
bar2 = plt.bar([i + bar_width / 2 for i in index], [metrics_team1[1], metrics_team2[1]], bar_width, label='Goals Conceded', color='red')

plt.xlabel('Teams')
plt.ylabel('Goals')
plt.title(f'Goals Scored vs. Goals Conceded ({SEASON})')
plt.xticks(index, TEAM_NAMES)
plt.legend()
plt.show()

# Pie chart for win/loss ratio
plt.figure(figsize=(14, 7))
plt.subplot(121)
plt.pie([metrics_team1[2], metrics_team1[3], metrics_team1[4]], labels=["Wins", "Losses", "Draws"], autopct='%1.1f%%', colors=['blue', 'red', 'gray'])
plt.title(f"{TEAM_NAMES[0]} Match Results Distribution ({SEASON})")

plt.subplot(122)
plt.pie([metrics_team2[2], metrics_team2[3], metrics_team2[4]], labels=["Wins", "Losses", "Draws"], autopct='%1.1f%%', colors=['blue', 'red', 'gray'])
plt.title(f"{TEAM_NAMES[1]} Match Results Distribution ({SEASON})")

plt.show()

