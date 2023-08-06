import xml.etree.ElementTree as ET 
import re
import pandas as pd
import numpy as np
from yahoo_oauth import OAuth2

ns = {'xlmns': 'http://fantasysports.yahooapis.com/fantasy/v2/base.rng',
      'yahoo': "http://www.yahooapis.com/v1/base.rng"}

oauth = OAuth2(None, None, from_file='oauth.json')
if not oauth.token_is_valid():
    oauth.refresh_access_token()

oc_mult = dict(zip(['QB','RB','WR','TE','K','DST'],[.3,.5,.5,.3,.15,.15]))

flex_positions = ['RB','WR','TE']
    
    
    
class YahooDraft:
    def __init__(self, league_id, my_first_pick):
        self.league_id = str(league_id)
        self.first_pick = my_first_pick
        self.my_team = my_first_pick
        self.league_url = f"https://fantasysports.yahooapis.com/fantasy/v2/league/nfl.l.{self.league_id}"
        self.get_settings()
        pass
    
    
    
    def get_settings(self):
        url = f"{self.league_url}/settings"
        r = oauth.session.get(url)
        xmlstring = r.text
        xmlstring = re.sub(' xmlns="[^"]+"', '', xmlstring, count=1)
        root = ET.fromstring(xmlstring)
        self.num_teams = int(root[0].find('num_teams').text)

        positions = {}
        settings = root[0].find('settings')
        rp = settings.find('roster_positions')
        
        yahoo_pos_map = {
            'QB':'QB',
            'WR':'WR',
            'RB':'RB',
            'TE':'TE',
            'W/R/T':'FLEX',
            'DEF':'DST',
            'K':'K',
            'BN':'BEN'
        }
        
        for c in rp:
            ypos = yahoo_pos_map[c[0].text]
            if ypos == 'BEN':
                positions[ypos] = int(c[1].text)
            else:
                positions[ypos] = int(c[2].text)
                
        self.req_positions = pd.Series(positions)
        
        self.rounds = self.req_positions.sum()
        self.pick_order = (list(range(1,self.num_teams+1)) + list(range(self.num_teams,0,-1))) * (self.rounds // 2)
        if self.rounds % 2 == 1:
            self.pick_order += list(range(1,self.num_teams+1))
        self.current_pick = 1
        pass
    
    
    
    def update(self, projections):
        self.scrape_draft()
        self.slot_needs(projections)
        projections = self.filter_players(projections)
        projections['need_adj'] = projections['position'].map(self.pos_needs['need'])
        return projections
        
    
    
    def scrape_draft(self):
        players = {}
        teams = self.num_teams
        for i in range(1,teams+1):
            _url = f"{self.league_url}/teams;team_keys=nfl.l.{self.league_id}.t.{i}/players"
            _r = oauth.session.get(_url)
            xmlstring = _r.text
            xmlstring = re.sub(' xmlns="[^"]+"', '', xmlstring, count=1)
            root = ET.fromstring(xmlstring)
            for player in root.iter('player_id'):
                players[player.text] = i
        self.picked_players = pd.Series(players, name='team')
        self.team_mask = self.picked_players == self.my_team
        self.team_roster = self.picked_players[self.team_mask]
        self.current_pick = self.picked_players.shape[0] + 1
        pass

    
    
    
    def slot_needs(self, projections):
        filled_slots = projections[projections['yahoo_id'].isin(self.team_roster.index)]['position'].value_counts()
        open_slots = self.req_positions.subtract(filled_slots, fill_value=0)

        needs = open_slots[['QB','RB','WR','TE','K','DST']]
        flex_need = needs[flex_positions].min() >= 0

        pos_needs = pd.DataFrame(open_slots > 0, columns=['slot'])
        pos_needs['flex'] = np.where(pos_needs.index.isin(flex_positions), flex_need, False)
        pos_needs['need'] = pos_needs['slot'] | pos_needs['flex']
        self.pos_needs = pos_needs
        pass
    
    
    
    def filter_players(self, projections):
        projections['picked'] = projections['yahoo_id'].isin(self.picked_players.index)
        return projections