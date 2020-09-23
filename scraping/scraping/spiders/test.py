import asyncio
import csv
import json

import aiohttp

from understat import Understat


csvheaders=['player id','position','team','assists','games','goals','key_passes','npg','npxg','red','season','shots','time','xa','xg','xgbuildup','xgchain','yellow',]
csvheaders2=['player id','shottype','assists','goals','key_passes','npg','npxg','season','shots','xa','xg',]
csvheaders3=['player id','shotzones','assists','goals','key_passes','npg','npxg','season','shots','xa','xg',]
position_file=open('Position_testfile.csv','w',encoding='utf-8',newline='')
season_file=open('Season_testfile.csv','w',encoding='utf-8',newline='')
shotzone_file=open('shotzone_testfile.csv','w',encoding='utf-8',newline='')
shottype_file=open('shottype_testfile.csv','w',encoding='utf-8',newline='')
writerP=csv.DictWriter(position_file,fieldnames=csvheaders)
writerP.writeheader()
writerS=csv.DictWriter(season_file,fieldnames=csvheaders)
writerS.writeheader()
writer_sz=csv.DictWriter(shotzone_file,fieldnames=csvheaders3)
writer_sz.writeheader()
writer_st=csv.DictWriter(shottype_file,fieldnames=csvheaders2)
writer_st.writeheader()


async def main():
    async with aiohttp.ClientSession() as session:
        understat = Understat(session)
        i=1
        while(i!=8697):
            player = await understat.get_player_grouped_stats(
                i
            )

            for key in [v for v in player.get('position',{}).keys()]:
                for pos in [v for v in (player.get('position',{}).get(key,{})).keys()]:
                    item = dict()
                    item['player id'] = i
                    item['position']=player.get('position',{}).get(key,{}).get(pos,{}).get('position')
                    item['assists'] = player.get('position',{}).get(key,{}).get(pos,{}).get('assists')
                    item['games'] = player.get('position',{}).get(key,{}).get(pos,{}).get('games')
                    item['goals'] = player.get('position',{}).get(key,{}).get(pos,{}).get('goals')
                    item['key_passes'] = player.get('position',{}).get(key,{}).get(pos,{}).get('key_passes')
                    item['npg'] = player.get('position',{}).get(key,{}).get(pos,{}).get('npg')
                    item['npxg'] = player.get('position',{}).get(key,{}).get(pos,{}).get('npxg')
                    item['red'] = player.get('position',{}).get(key,{}).get(pos,{}).get('red')
                    item['season'] = player.get('position',{}).get(key,{}).get(pos,{}).get('season')
                    item['shots'] = player.get('position',{}).get(key,{}).get(pos,{}).get('shots')
                    item['time'] = player.get('position',{}).get(key,{}).get(pos,{}).get('time')
                    item['xa'] = player.get('position',{}).get(key,{}).get(pos,{}).get('xA')
                    item['xg'] = player.get('position',{}).get(key,{}).get(pos,{}).get('xG')
                    item['xgbuildup'] = player.get('position',{}).get(key,{}).get(pos,{}).get('xGBuildup')
                    item['xgchain'] = player.get('position',{}).get(key,{}).get(pos,{}).get('xGChain')
                    item['yellow'] = player.get('position',{}).get(key,{}).get(pos,{}).get('yellow')
                    item['team'] = player.get('position',{}).get(key,{}).get(pos,{}).get('team')
                    writerP.writerow(item)
                    position_file.flush()
                    print(item)

            for seas in player.get('season',{}):
                item1=dict()
                item1['player id'] = i
                item1['assists'] = seas.get('assists')
                item1['games']=seas.get('games')
                item1['goals']=seas.get('goals')
                item1['key_passes']=seas.get('key_passes')
                item1['npg']=seas.get('npg')
                item1['npxg']=seas.get('npxG')
                item1['red']=seas.get('red')
                item1['season']=seas.get('season')
                item1['shots']=seas.get('shots')
                item1['time']=seas.get('time')
                item1['xa']=seas.get('xA')
                item1['xg']=seas.get('xG')
                item1['xgbuildup']=seas.get('xGBuildup')
                item1['xgchain']=seas.get('xGChain')
                item1['yellow']=seas.get('yellow')
                item1['team']=seas.get('team')
                item1['position']=seas.get('position')
                writerS.writerow(item1)
                season_file.flush()

            for SZone in [v for v in player.get('shotZones',{}).keys()]:
                for SzoneShot in [v for v in player.get('shotZones',{}).get(SZone,{}).keys()]:
                    item2=dict()
                    item2['player id']=i
                    item2['shotzones']=player.get('shotZones',{}).get(SZone,{}).get(SzoneShot,{}).get('shotZones')
                    item2['assists']=player.get('shotZones',{}).get(SZone,{}).get(SzoneShot,{}).get('assists')
                    item2['goals']=player.get('shotZones',{}).get(SZone,{}).get(SzoneShot,{}).get('goals')
                    item2['key_passes']=player.get('shotZones',{}).get(SZone,{}).get(SzoneShot,{}).get('key_passes')
                    item2['npg']=player.get('shotZones',{}).get(SZone,{}).get(SzoneShot,{}).get('npg')
                    item2['npxg']=player.get('shotZones',{}).get(SZone,{}).get(SzoneShot,{}).get('npxG')
                    item2['season']=player.get('shotZones',{}).get(SZone,{}).get(SzoneShot,{}).get('season')
                    item2['shots']=player.get('shotZones',{}).get(SZone,{}).get(SzoneShot,{}).get('shots')
                    item2['xa']=player.get('shotZones',{}).get(SZone,{}).get(SzoneShot,{}).get('xA')
                    item2['xg']=player.get('shotZones',{}).get(SZone,{}).get(SzoneShot,{}).get('xG')
                    writer_sz.writerow(item2)
                    shotzone_file.flush()

            for Stype in [v for v in player.get('shotTypes',{}).keys()]:
                for StypeShot in [v for v in player.get('shotTypes', {}).get(Stype, {}).keys()]:
                    item3=dict()
                    item3['player id'] = i
                    item3['shottype'] = player.get('shotTypes', {}).get(Stype, {}).get(StypeShot, {}).get('shotTypes')
                    item3['assists'] = player.get('shotTypes', {}).get(Stype, {}).get(StypeShot, {}).get('assists')
                    item3['goals'] = player.get('shotTypes', {}).get(Stype, {}).get(StypeShot, {}).get('goals')
                    item3['key_passes'] = player.get('shotTypes', {}).get(Stype, {}).get(StypeShot, {}).get(
                        'key_passes')
                    item3['npg'] = player.get('shotTypes', {}).get(Stype, {}).get(StypeShot, {}).get('npg')
                    item3['npxg'] = player.get('shotTypes', {}).get(Stype, {}).get(StypeShot, {}).get('npxG')
                    item3['season'] = player.get('shotTypes', {}).get(Stype, {}).get(StypeShot, {}).get('season')
                    item3['shots'] = player.get('shotTypes', {}).get(Stype, {}).get(StypeShot, {}).get('shots')
                    item3['xa'] = player.get('shotTypes', {}).get(Stype, {}).get(StypeShot, {}).get('xA')
                    item3['xg'] = player.get('shotTypes', {}).get(Stype, {}).get(StypeShot, {}).get('xG')
                    writer_st.writerow(item3)
                    shottype_file.flush()
            i=i+1


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
