# Imports
from classes.Cricketer import Cricketer
import pandas as pd
import argparse # Allow for the passing of the player_id
import re

# Add all the relevant arguments to pass in for the command line 
a = argparse.ArgumentParser(description='south_african_bowlers.py')
a.add_argument("--player_id", action="store", type=str, required=True)

# Define those arguments as variables for use in the script
arguments = a.parse_args()


base_innings_by_innings = 'http://stats.espncricinfo.com/ci/engine/player/%s.html?class=1;template=results;type=allround;view=innings'
rabada_id = arguments.player_id #'550215'

rabada = Cricketer(base_innings_by_innings % rabada_id)
name_script = [x.text for x in rabada.soup.find_all('script') if x.text.find('Test matches:All-round records') >= 0][0]
name = re.compile('.*Test matches\:All\-round records:(.*)\"\;.*').search(name_script).group(1)

# Print name of Cricketer to terminal 
print('='*len(name))
print(name)
print('='*len(name) + '\n')

rabada_innings = rabada.innings()
rabada_bowling = rabada_innings[rabada_innings.did_bowl].copy()

# Get all the matches from the innings 
matches = rabada.get_test_matches()

# Loop through the bowling innings and find the relevant stats
full_stats = []
for i in range(0,len(rabada_bowling)):
    this_innings = rabada_bowling.iloc[i]
    innings_index = this_innings.name
    n_inns = this_innings.inns
    match_id = this_innings.match_id
    match_obj = matches[match_id]
    scorecard = match_obj.select_innings(int(n_inns)).bowling()
    specific_score = scorecard[scorecard.player_id == rabada_id]
    # Total balls
    full_stats.append({'total_balls':specific_score.total_balls.item()})
    
rabada_bowling['extra_stats'] = full_stats 
final = pd.concat([rabada_bowling, rabada_bowling.extra_stats.apply(pd.Series)], axis = 1).drop('extra_stats', axis = 1)

#print(final[['overs', 'total_balls', 'conc', 'wkts', 'opposition']])

conc = rabada_bowling.conc.astype(int).sum()
wkts = rabada_bowling.wkts.astype(int).sum()
total_balls = final.total_balls.astype(int).sum()

print('Total runs conceeded: %d' % conc)
print('Total wickets: %d' % wkts)
print('Total balls bowled: %d' % total_balls)