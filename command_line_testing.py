from classes.Cricketer import Cricketer

joe_root = 'http://stats.espncricinfo.com/ci/engine/player/303669.html?class=1;template=results;type=allround;view=innings'

print(Cricketer(joe_root).rolling_average_matches(5))

print(Cricketer(joe_root).acc_yearly_conversion())