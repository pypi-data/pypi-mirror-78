
import yahoowizard.draft_logic as dl
from .update_probabilities import *
from .process_and_map_projections import *
from .yahoo_draft import *

def tell_me_what_to_do(players,prob,draft):
    players = draft.update(players)
    np1, np2 = dl.next_picks(draft.pick_order,draft.my_team, draft.current_pick)
    px = dl.adj_probs(players,prob,np1,np2)
    print(f'this pick is {draft.current_pick}')
    print(f'Your Next Pick is {np1}')
    print(f'Your 2nd Pick is {np2}')
    return px

def unblacklist_player(name,team,df):
    name_match = df['player'] == name
    team_match = df['team'] == team
    mask = name_match & team_match
    print("Removing these players from the blacklist:")
    print(df[mask][['player','team','position']])
    df['blacklist'] = np.where(mask, False, df['blacklist'])
    return df

def blacklist_player(name,team,df):
    name_match = df['player'] == name
    team_match = df['team'] == team
    mask = name_match & team_match
    print("Blacklisting these players:")
    print(df[mask][['player','team','position']])
    df['blacklist'] = np.where(mask, True, df['blacklist'])
    return df

def blacklist_position(position):
    "positions can be: 'QB','RB','WR','TE','DST','K'"
    df['blacklist'] = np.where(df['position'] == position, True, df['blacklist'])
    return df

def unblacklist_position(position):
    "positions can be: 'QB','RB','WR','TE','DST','K'"
    df['blacklist'] = np.where(df['position'] == position, False, df['blacklist'])