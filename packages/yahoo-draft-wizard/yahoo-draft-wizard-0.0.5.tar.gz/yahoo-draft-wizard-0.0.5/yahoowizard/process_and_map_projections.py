import pandas as pd
import numpy as np

oc_mult = dict(zip(['QB','RB','WR','TE','K','D/ST'],[.3,.5,.5,.3,.15,.15]))

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
    id_map = pd.read_json('nfl.json').T
    idcols = ['player_id','stats_id','yahoo_id','espn_id','rotowire_id','rotoworld_id','fantasy_data_id','sportradar_id']
    proj = proj.merge(id_map[idcols].astype(str), how='left', on='espn_id')
    print("3 of 4: saving pickle")
    proj.to_pickle(output_path)
    print("4 of 4: done")
    pass




