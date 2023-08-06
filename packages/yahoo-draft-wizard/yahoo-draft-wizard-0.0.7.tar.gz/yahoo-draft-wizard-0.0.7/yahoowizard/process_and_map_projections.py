import pandas as pd
import numpy as np

oc_mult = dict(zip(['QB','RB','WR','TE','K','D/ST'],[2/3, 1/4, 1/4, 2/3, 1, 1]))

def process_projections(projection_path,idmap_path,output_path):
    print("1 of 4: reading projections")
    proj = pd.read_csv(projection_path)
    proj = proj[proj['position'].isin(['RB','QB','WR','TE','K','DST'])]

    print("2 of 4: reading id mapping")
    espnidmap = pd.read_csv(idmap_path)

    proj = proj.merge(espnidmap, how='left', on='player')
    proj = proj[proj['rank'] <= 250]
    proj = proj.drop_duplicates(subset=['player','team','position'])
    proj = proj[proj['rank'] <= 250]
    proj = proj.sort_values('points', ascending=False)
    proj['picked'] = False
    proj['blacklist'] = False
    proj['espn_id'] = proj['espn_id'].astype(str)
    proj['oc_mult'] = proj['position'].map(oc_mult)
    proj.index = proj['espn_id']
    proj.index.name = None
    id_map = pd.read_excel('broad_id_map.xlsx', dtype=str)
    proj = proj.merge(id_map, how='left', on='espn_id')
    proj.index = proj['espn_id']
    proj.index.name = None
    print("3 of 4: saving pickle")
    proj.to_pickle(output_path)
    print("4 of 4: done")
    pass




