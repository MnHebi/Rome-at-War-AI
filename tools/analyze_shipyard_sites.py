"""Offline spatial evidence, not an engine buildability simulator.

Reads the initial terrain grid and sampled Shipyard rejection tuples. Dynamic
occupancy, exploration, resources and building completion are not reconstructed.
Output must stay outside the AI repository because it includes replay map data.
"""
import argparse
import collections
import csv
import json
import math
from pathlib import Path
import re
import sys


def rejection_records(chats):
    pending, current, records = {}, {}, []
    for chat in chats:
        player = chat.get('player')
        key = re.fullmatch(r'RAW12 diag id: (-?\d+)', chat['message'])
        value = re.fullmatch(r'RAW12 diag value: (-?\d+)', chat['message'])
        if key:
            pending[player] = int(key[1])
        if not value or player not in pending:
            continue
        key, value = pending.pop(player), int(value[1])
        if key == 545:
            current[player] = dict(player=player, time=chat['time'], reason=value)
        elif key in (536, 537, 538, 540) and player in current:
            current[player][{536: 'x', 537: 'y', 538: 'anchor', 540: 'attempt'}[key]] = value
            if key == 540:
                record = current.pop(player)
                if all(k in record for k in ('x', 'y', 'anchor')):
                    records.append(record)
    return records


def classify_point(x, y, dimension, tiles):
    x, y = math.floor(x), math.floor(y)
    if not (0 <= x < dimension and 0 <= y < dimension):
        return dict(terrain=-1, spatial_class='outside-map')
    terrain, elevation = tiles[y * dimension + x]
    # Current RaW DAT: restriction 6 permits these terrain IDs. DOCK2 has
    # placement terrain (1,4), side terrain (2,35), collision radii (1.5,1.5).
    # Only label clear misses; this deliberately does not assert valid sites.
    water = {1, 4, 22, 23}
    nearby = [tiles[yy * dimension + xx][0]
              for yy in range(max(0, y-2), min(dimension, y+3))
              for xx in range(max(0, x-2), min(dimension, x+3))]
    if terrain not in water | {2, 35}:
        kind = 'land-center'
    elif all(t in water for t in nearby):
        kind = 'water-without-nearby-shore'
    else:
        kind = 'coastal-or-mixed-unresolved'
    return dict(terrain=terrain, elevation=elevation, spatial_class=kind)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('parser_root', type=Path)
    parser.add_argument('replay', type=Path)
    parser.add_argument('decoded', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--render', action='store_true', help='Render map PNGs (requires Pillow).')
    args = parser.parse_args()
    sys.path.insert(0, str(args.parser_root))
    from mgz.fast import header
    with args.replay.open('rb') as stream:
        raw = header.decompress(stream)
        version, _, save, _ = header.parse_version(raw, stream)
        header.parse_de(raw, version, save)
        header.parse_metadata(raw, save)
        terrain_map = header.parse_map(raw, version, save)
    data = json.loads(args.decoded.read_text(encoding='utf-8'))
    records = rejection_records(data['chats'])
    dimension, tiles = terrain_map['dimension'], terrain_map['tiles']
    for record in records:
        record.update(classify_point(record['x'], record['y'], dimension, tiles))
    builds = [dict(a, **classify_point(a['x'], a['y'], dimension, tiles))
              for a in data['build_actions'] if a['building_id'] == 1251]
    summary = {'dimension': dimension, 'rejections': len(records), 'players': {}, 'builds': builds}
    for player in range(1, 9):
        rejected = [r for r in records if r['player'] == player and r['reason'] == 64]
        summary['players'][player] = dict(reason64=len(rejected),
            terrain=dict(collections.Counter(r['terrain'] for r in rejected)),
            spatial=dict(collections.Counter(r['spatial_class'] for r in rejected)))
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / 'summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    with (args.output / 'candidates.csv').open('w', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=['player','time','reason','x','y','anchor','attempt','terrain','elevation','spatial_class'])
        writer.writeheader()
        writer.writerows(records)
    print(json.dumps(summary, indent=2))
    if not args.render:
        return
    # Pixel-exact terrain grid with conventional replay axes, not an isometric
    # screenshot. Three confirmed build sites provide coordinate controls.
    from PIL import Image, ImageDraw, ImageColor
    colors = {1:'#6bbada',23:'#398dc6',22:'#276499',2:'#efda9c',4:'#9dc9b8',19:'#225522',88:'#31602d'}
    scale=5
    for player in range(1,9):
        im=Image.new('RGB',(dimension,dimension))
        im.putdata([ImageColor.getrgb(colors.get(t[0], '#9eae74')) for t in tiles])
        im=im.resize((dimension*scale,dimension*scale),Image.Resampling.NEAREST)
        draw=ImageDraw.Draw(im)
        for r in records:
            if r['player'] != player: continue
            x,y=r['x']*scale,r['y']*scale
            draw.line((x-2,y-2,x+2,y+2),fill='red')
            draw.line((x-2,y+2,x+2,y-2),fill='red')
        for b in builds:
            if b['player_id'] != player: continue
            x,y=b['x']*scale,b['y']*scale
            draw.ellipse((x-7,y-7,x+7,y+7),outline='white',width=3)
            draw.text((x+9,y),b['time'],fill='white')
        draw.text((5,5),f'P{player}: red=rejected samples, white=issued Shipyard; X right, Y down',fill='black')
        im.save(args.output / f'player-{player}.png')


if __name__ == '__main__':
    main()
