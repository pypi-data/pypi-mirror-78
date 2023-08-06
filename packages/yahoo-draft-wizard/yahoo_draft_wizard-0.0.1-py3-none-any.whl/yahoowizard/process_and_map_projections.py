import pandas as pd
import numpy as np

oc_mult = dict(zip(['QB','RB','WR','TE','K','D/ST'],[.3,.5,.5,.3,.15,.15]))


def process_projections(projection_path,idmap_path,output_path):
    proj = pd.read_csv(projection_path)
    proj = proj[proj['position'].isin(['RB','QB','WR','TE','K','DST'])]

    espnidmap = pd.read_csv(idmap_path)

    proj = proj.merge(espnidmap, how='left', on='player')
    proj = proj.dropna(subset=['adp'])
    proj = proj.drop_duplicates(subset=['playerId'])
    proj['picked'] = False
    proj['blacklist'] = False
    proj['espn_id'] = proj['espn_id'].astype(str)
    proj['oc_adj'] = proj['position'].map(oc_mult)
    
    id_map = pd.read_json('nfl.json').T
    idcols = ['player_id','stats_id','yahoo_id','espn_id','rotowire_id','rotoworld_id','fantasy_data_id','sportradar_id']
    
    proj = proj.merge(id_map[idcols].astype(str), how='left', on='espn_id')
    proj.to_pickle(output_path)
    pass




