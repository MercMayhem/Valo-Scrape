from vlrscrape import vlrscrape
import pandas as pd

links = [
    'https://www.vlr.gg/220441/paper-rex-vs-drx-champions-tour-2023-masters-tokyo-ubqf',
    'https://www.vlr.gg/220442/fnatic-vs-nrg-esports-champions-tour-2023-masters-tokyo-ubqf',
    'https://www.vlr.gg/220443/team-liquid-vs-edward-gaming-champions-tour-2023-masters-tokyo-ubqf',
    'https://www.vlr.gg/220444/loud-vs-evil-geniuses-champions-tour-2023-masters-tokyo-ubqf',
    'https://www.vlr.gg/220445/paper-rex-vs-fnatic-champions-tour-2023-masters-tokyo-ubsf',
    'https://www.vlr.gg/220446/team-liquid-vs-evil-geniuses-champions-tour-2023-masters-tokyo-ubsf',
    'https://www.vlr.gg/220447/fnatic-vs-evil-geniuses-champions-tour-2023-masters-tokyo-ubf',
    'https://www.vlr.gg/220448/fnatic-vs-evil-geniuses-champions-tour-2023-masters-tokyo-gf'
    'https://www.vlr.gg/220449/drx-vs-nrg-esports-champions-tour-2023-masters-tokyo-lr1',
    'https://www.vlr.gg/220450/edward-gaming-vs-loud-champions-tour-2023-masters-tokyo-lr1',
    'https://www.vlr.gg/220451/team-liquid-vs-nrg-esports-champions-tour-2023-masters-tokyo-lr2',
    'https://www.vlr.gg/220452/paper-rex-vs-edward-gaming-champions-tour-2023-masters-tokyo-lr2',
    'https://www.vlr.gg/220453/nrg-esports-vs-paper-rex-champions-tour-2023-masters-tokyo-lr3',
    'https://www.vlr.gg/220454/evil-geniuses-vs-paper-rex-champions-tour-2023-masters-tokyo-lbf'
]
final_df = []

for link in links:
    final_df.append(vlrscrape(link))

final_df = pd.concat(final_df, ignore_index=True, axis=0)

for column in final_df.select_dtypes(object):
    final_df.loc[:, column] = final_df[column].str.replace('\n', ' ')

final_df.to_csv('test.csv', index=False)

# print(final_df[0])
