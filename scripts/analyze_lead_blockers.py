import pandas as pd
from shapely.geometry import Point
import numpy as np

# Set display options for pandas
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)

# Replace these paths with your actual file paths
tracking_data_path = '../tracking_week_9.csv'
motion_players_path = '../motion-players.csv'
player_play_path = '../player_play.csv'

# Load the data
tracking_data = pd.read_csv(tracking_data_path)
motion_players = pd.read_csv(motion_players_path)
player_play = pd.read_csv(player_play_path)

# Function to check if a motion player stays in the blocking cone and is ahead of the ball carrier
def is_in_blocking_cone_and_ahead(motion_row, ball_row, direction_tolerance):
    angle_diff = abs(motion_row['o'] - ball_row['o'])
    angle_diff = min(angle_diff, 360 - angle_diff)  # Handle circular nature of angles
    is_in_cone = angle_diff <= direction_tolerance  # Check if within direction tolerance
    is_ahead = motion_row['x'] > ball_row['x'] if ball_row['o'] < 180 else motion_row['x'] < ball_row['x']
    return is_in_cone and is_ahead

# Analyze a single play
def analyze_play(game_id, play_id, tolerance=0.3, direction_tolerance=45, debug=False):
    try:
        if debug:
            print(f"DEBUG: Starting analysis for gameId: {game_id}, playId: {play_id} with tolerance={tolerance}")

        # Step 1: Get motion player
        motion_player_data = motion_players[
            (motion_players['gameId'] == game_id) & (motion_players['playId'] == play_id)
        ]
        if motion_player_data.empty:
            return {"gameId": game_id, "playId": play_id, "result": "No motion player found"}

        motion_player_id = motion_player_data['nflId'].iloc[0]

        # Step 2: Get ball carrier
        ball_carrier_data = player_play[
            (player_play['gameId'] == game_id) & (player_play['playId'] == play_id) & (player_play['hadRushAttempt'] == True)
        ]
        if ball_carrier_data.empty:
            return {"gameId": game_id, "playId": play_id, "result": "No ball carrier found"}

        ball_carrier_id = ball_carrier_data['nflId'].iloc[0]

        # Step 3: Filter tracking data
        tracking_play_data = tracking_data[
            (tracking_data['gameId'] == game_id) & (tracking_data['playId'] == play_id)
        ]
        motion_player_path = tracking_play_data[tracking_play_data['nflId'] == motion_player_id]
        ball_carrier_path = tracking_play_data[tracking_play_data['nflId'] == ball_carrier_id]

        if motion_player_path.empty or ball_carrier_path.empty:
            return {"gameId": game_id, "playId": play_id, "result": "No tracking data for players"}

        # Step 4: Detect intersections and direction filter
        intersections = []
        for _, motion_row in motion_player_path.iterrows():
            for _, ball_row in ball_carrier_path.iterrows():
                distance_squared = (motion_row['x'] - ball_row['x']) ** 2 + (motion_row['y'] - ball_row['y']) ** 2
                if distance_squared <= tolerance ** 2:
                    if is_in_blocking_cone_and_ahead(motion_row, ball_row, direction_tolerance):
                        intersections.append({
                            "frameId": motion_row['frameId'],
                            "motion_x": motion_row['x'],
                            "motion_y": motion_row['y'],
                            "ball_x": ball_row['x'],
                            "ball_y": ball_row['y'],
                            "motion_dir": motion_row['o'],
                            "ball_dir": ball_row['o']
                        })

        if debug:
            print(f"DEBUG: Intersections found: {len(intersections)}")
            for intersection in intersections[:10]:
                print(
                    f"DEBUG: Intersection at frame {intersection['frameId']}: Motion ({intersection['motion_x']}, {intersection['motion_y']}, Direction: {intersection['motion_dir']}), "
                    f"Ball ({intersection['ball_x']}, {intersection['ball_y']}, Direction: {intersection['ball_dir']})"
                )

        if not intersections:
            return {"gameId": game_id, "playId": play_id, "result": "No intersections found"}

        # Step 5: Determine lead blocker
        for intersection in intersections:
            motion_frame = intersection['frameId']
            ball_frame = ball_carrier_path[ball_carrier_path['frameId'] >= motion_frame]['frameId'].min()
            if pd.notna(ball_frame) and ball_frame >= motion_frame:
                return {"gameId": game_id, "playId": play_id, "result": f"Lead Blocker Detected at Frame: {motion_frame}"}

        return {"gameId": game_id, "playId": play_id, "result": "No valid lead blocker motion detected"}
    except Exception as e:
        return {"gameId": game_id, "playId": play_id, "result": f"Error: {str(e)}"}

# Analyze all plays for all games
results = []
tolerance = 0.3  # Adjust as needed
direction_tolerance = 45  # Adjust as needed

game_ids = tracking_data['gameId'].unique()
for game_id in game_ids:
    play_ids = tracking_data[tracking_data['gameId'] == game_id]['playId'].unique()
    for play_id in play_ids:
        print(f"Processing gameId: {game_id}, playId: {play_id}")
        result = analyze_play(game_id, play_id, tolerance, direction_tolerance, debug=False)
        results.append(result)

# Save results to a DataFrame and export to CSV
results_df = pd.DataFrame(results)

# Count plays with a lead blocker
lead_blocker_count = results_df['result'].str.contains("Lead Blocker Detected").sum()
total_eligible_plays = len(results_df[~results_df['result'].str.contains("No motion player found|No ball carrier found")])

print(f"Total plays with a lead blocker: {lead_blocker_count}")
print(f"Total eligible plays: {total_eligible_plays}")
print(f"Percentage of plays with a lead blocker: {lead_blocker_count / total_eligible_plays:.2%}")


