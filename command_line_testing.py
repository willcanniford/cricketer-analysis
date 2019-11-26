from CricketPlayer import CricketPlayer

joe_root = 'http://stats.espncricinfo.com/ci/engine/player/303669.html?class=1;template=results;type=allround;view=innings'

print(CricketPlayer(joe_root).rolling_average_matches(5))