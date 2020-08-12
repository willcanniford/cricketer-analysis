import helpers.batting as bat
import helpers.visuals as vis
import helpers.bowling as bowl
import helpers.scrapers as scrape
import matplotlib.pyplot as plt
import numpy as np

# jim_bowling = bowl.test_innings_by_innings(8608, home_or_away=1)
# print(jim_bowling.head())
# print(bowl.test_home_or_away(210283))


# Columns to keep
# How to format each column

schema = {
    'original_name': 'Runs',
    'new_name': 'runs',
    'data_type': 'int',
    'regex_clean': '',
    "na_values": ['DNB']
}

# innings = bat.test_innings_by_innings(519082)
# jos = bat.odi_innings_by_innings(308967, home_or_away=2)

# batted = jos.runs.notnull()
# did_not_bat = jos.runs.isnull()

# jos_batted = jos[batted]
# print(jos_batted.head())

morgan = bat.odi_innings_by_innings(24598)
morgan_trim = morgan[morgan.score.notnull()]
career_strike_rate = bat.summarise(morgan)['strike_rate'] * 100
career_high_score_lim = bat.summarise(morgan)['high_score'] * 1.15

more_balls = morgan_trim[morgan_trim.balls_faced.astype(int) >= 15]
career_sr_series = more_balls.score.astype(int) / more_balls.balls_faced.astype(int) * 100.0
# plt.boxplot(career_sr_series)
# print(career_sr_series.quantile(0.25))
# print(career_sr_series.quantile(0.75))

plt.scatter(morgan_trim.balls_faced.astype(int), morgan_trim.score.astype(int), s=3,
            marker="D", zorder=100, c="#1976D2")
# plot_strike_rate_line(80, 175, 175, c="#d1ccc0", linestyle='dashed', alpha=0.75, zorder=0)
vis.plot_strike_rate_line(career_strike_rate, 175, 175, c="#E64A19", linestyle='dashed', alpha=0.75, zorder=1,
                          label="Career Strike Rate")
# plot_strike_rate_line(100, 175, 175, c="#d1ccc0", linestyle='dashed', alpha=0.75, zorder=0)
# plot_strike_rate_line(120, 175, 175, c="#d1ccc0", linestyle='dashed', alpha=0.75, zorder=0)
# plot_strike_rate_line(140, 175, 175, c="#d1ccc0", linestyle='dashed', alpha=0.75, zorder=0)
# plt.hist(morgan_trim.score.astype(int), bins=30)

vis.plot_strike_rate_line(career_sr_series.quantile(0.25), 175, 175, c="#616161", linestyle='dashed', alpha=0.75,
                          zorder=0, label='25% percentile (Innings >= 15 balls)')
vis.plot_strike_rate_line(career_sr_series.quantile(0.75), 175, 175, c="#616161", linestyle='dashed', alpha=0.75,
                          zorder=0, label='75% percentile (Innings >= 15 balls)')
vis.plot_strike_rate_line(career_sr_series.quantile(0.50), 175, 175, c="#388E3C", linestyle='dashed', alpha=0.75,
                          zorder=0, label='Median (Innings >= 15 balls)')

# median_balls = morgan_trim.balls_faced.astype(int).median()
# median_runs = morgan_trim.score.astype(int).median()
# plt.axvline(median_balls)
# plt.axhline(median_runs)

plt.xlim(0, 175)
plt.ylim(0, 175)
plt.ylabel('Runs')
plt.xlabel('Balls Faced')
plt.legend(fontsize='x-small')
plt.savefig('morgan_ODI.png', dpi=150)
