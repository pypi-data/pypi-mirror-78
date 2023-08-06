import pandas as pd
import numpy as np


def next_picks(pick_order, mypick, thispick):
    next_pick = pick_order.index(mypick,thispick) + 1
    next_pick2 = pick_order.index(mypick,next_pick) + 1
    return next_pick, next_pick2

def p2f(x):
    return float(x.strip('%'))/100

def expected_max(df):
    df['pbest'] = df['probpicked'].cumprod().shift().fillna(1)
    df['emaxw'] = df['pbest'] * df['%']
    df['emax'] = df['points'] * df['emaxw']
    return df

def adj_probs(players,probs, next_pick, next_pick2):
    # players['oc_adj'] = players['need_adj']*1 + ~players['need_adj']*players['oc_mult']
    players['penalty'] = players['oc_mult'] * players['bench_count']
    players['penalty'] = np.clip(players['penalty'], 0, 1)
    players['oc_adj'] = 1 - players['penalty']
    players['espn_id'] = players['espn_id'].astype(str)
    probs['espnid'] = probs['espnid'].astype(str)
    for i, pick in enumerate([next_pick,next_pick2]):
        pmask = probs['pick'] == pick
        df = players.merge(probs[pmask], how='left', left_on='espn_id', right_on='espnid')
        df = df.drop_duplicates(subset=['player','team'])
        df = df.drop_duplicates(subset=['espn_id'])
        df.index = df['espn_id']
        df.index.name = None
        df['%'] = df['%'].fillna(1)
        df['%'] = np.where(df['picked'] | df['blacklist'], 0, df['%'])
        df['probpicked'] = 1 - df['%']
        df = df.groupby('position').apply(expected_max)
        df.index = df['espn_id']
        df.index.name = None
        palt = df.groupby('position')['emax'].sum()
        df['opp'] = df['position'].map(palt)
        players[f'oc_raw_{i}'] = (df['points'] - df['opp']) * ~df['picked'] * ~df['blacklist']
        players[f'pb_{i}'] = df['probpicked']
        players[f'oc_adj_{i}'] = players[f'oc_raw_{i}'] * players['oc_adj'] * players[f'pb_{i}']
    return players.copy()


