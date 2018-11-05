#!/usr/bin/env python3

"""
TODO: perhaps rely on latest candidates.json first? ran into John Lewis case

-L000287,833
+L000287,63728

TODO: two legislators are removed

W000413, T000473
"""

import os, csv, json, itertools

from blessings import Terminal
t = Terminal()

DATA_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')

with open(DATA_FOLDER + '/legislators-2016.json') as f:
    legislators_2016 = json.load(f)

with open(DATA_FOLDER + '/legislators-current.json') as f:
    legislators_current = json.load(f)

with open(DATA_FOLDER + '/ap_candidates.csv') as f:
    reader = csv.DictReader(f)
    ap_candidates = [row for row in reader]

with open(DATA_FOLDER + '/ap_historical_ids.csv') as f:
    reader = csv.DictReader(f)
    ap_candidates2 = [row for row in reader]

# make quotes dumb for candidates
for c in ap_candidates:
    for field in ['first_name', 'middle_name', 'last_name', 'suffix']:
        if c.get(field):
            c[field] = c[field].replace("’", "'")
            c[field] = c[field].replace("á", "a")

# make quotes dumb for legislators
for l in legislators_2016 + legislators_current:
    for field in ['first', 'middle', 'last', 'suffix']:
        if l['name'].get(field):
            l['name'][field] = l['name'][field].replace("’", "'")
            l['name'][field] = l['name'][field].replace("á", "a")

key=lambda x: (x['first_name'], x['middle_name'], x['last_name'], x['suffix'],)
mapping1 = {k:tuple(v) for k,v in itertools.groupby(sorted(ap_candidates, key=key), key=key)}

key=lambda x: (x['first_name'], x['middle_name'], x['last_name'],)
mapping2 = {k:tuple(v) for k,v in itertools.groupby(sorted(ap_candidates, key=key), key=key)}

key=lambda x: (x['first_name'], x['last_name'],)
mapping3 = {k:tuple(v) for k,v in itertools.groupby(sorted(ap_candidates, key=key), key=key)}

key=lambda x: (x['name'],)
mapping4 = {k:tuple(v) for k,v in itertools.groupby(sorted(ap_candidates2, key=key), key=key)}

key=lambda x: (x['nickname'] + ' ' + x['name'].split(' ')[-1],)
mapping5 = {k:tuple(v) for k,v in itertools.groupby(sorted([x for x in ap_candidates2 if x['nickname']], key=key), key=key)}

manual_mapping = {
    "C000567": 690,
    "C001070": 39527,
    "A000360": 1421,
    "C001035": 1727,
    "D000563": 1262,
    "E000285": 508,
    "I000024": 1048,
    "M000355": 210,
    "R000122": 964,
    "C001088": 60997,
    "B001251": 34352,
    "C001037": 889,
    "C001072": 57849,
    "C001049": 1337,
    "C000537": 1414,
    "C000542": 18782,
    "C001062": 1860,
    "C001087": 60226,
    "F000459": 60964,
    "F000445": 711,
    "G000568": 58574,
    "G000551": 1131,
    "G000535": 1267,
    "H001055": 60689,
    "H001047": 59590,
    "H000636": 304,
    "H001034": 1206,
    "H001048": 59681,
    "J000288": 59400,
    "K000375": 22757,
    "L000573": 60527,
    "L000566": 57148,
    "L000565": 51537,
    "L000570": 56805,
    "M000312": 883,
    "M000702": 1726,
    "P000588": 31918,
    "R000578": 50215,
    "R000146": 1741,
    "R000589": 60318,
    "R000582": 59572,
    "R000583": 59163,
    "R000487": 1215,
    "R000576": 1055,
    "S000244": 1099,
    "S000248": 1545,
    "S001148": 504,
    "S001156": 116,
    "T000462": 411,
    "T000461": 257,
    "T000463": 1376,
    "V000081": 1535,
    "V000127": 906,
    "W000799": 51531,
    "P000604": 382,
    "L000578": 52531,
    "C001097": 6688,
    "K000379": 60122,
    "N000127": 62587,
    "B001288": 63133,
    "D000613": 60158,
    "T000473": 53363,
    "S001198": 64262,
    "E000295": 63566,
    "D000625": 32620,
    "C001110": 20657,
    "B001303": 65591,
    "E000298": 6662,
    "H001079": 28529,
    "N000190": 51896,
    "H001078": 61015,
    "G000585": 65841,
    "S001203": 66096,
    "C001114": 44042,
    "G000580": 65420,
    "M001200": 45762,
    "G000583": 65116,
    "F000465": 64902,
    "L000287": 833,
}

rows = []

for i, d in enumerate(legislators_2016 + legislators_current):

    if d['terms'][-1]['state'] in ['VI', 'PR', 'AS', 'GU', 'MP']: continue

    bioguide_id = d['id']['bioguide']
    name = d['name']
    first = name['first']
    middle = name.get('middle', '')
    last = name['last']
    suffix = name.get('suffix', '')
    full = name['official_full']
    
    if manual_mapping.get(bioguide_id):
        pol_id = manual_mapping[bioguide_id]
        print(i, "found", bioguide_id, pol_id)
        rows.append([bioguide_id, pol_id])
    elif mapping1.get((first, middle, last, suffix,)):
        ap_cands = mapping1[(first, middle, last, suffix,)]
        pol_id = ap_cands[0]['pol_id']
        print(i, "found", bioguide_id, pol_id)
        rows.append([bioguide_id, pol_id])
    elif mapping2.get((first, middle, last,)):
        ap_cands = mapping2[(first, middle, last,)]
        pol_id = ap_cands[0]['pol_id']
        print(i, "found", bioguide_id, pol_id)
        rows.append([bioguide_id, pol_id])
    elif mapping3.get((first, last,)):
        ap_cands = mapping3[(first, last,)]
        pol_id = ap_cands[0]['pol_id']
        print(i, "found", bioguide_id, pol_id)
        rows.append([bioguide_id, pol_id])
    elif mapping4.get((full,)):
        ap_cands = mapping4[(full,)]
        pol_id = ap_cands[0]['pol_id']
        print(i, "found",bioguide_id, pol_id)
        rows.append([bioguide_id, pol_id])
    elif mapping5.get((full,)):
        ap_cands = mapping5[(full,)]
        pol_id = ap_cands[0]['pol_id']
        print(i, "found", bioguide_id, pol_id)
        rows.append([bioguide_id, pol_id])
    else:
        print(i, t.red("not found"), d['id']['bioguide'], "First:", first, "|", "Middle:", middle,  "|", "Last:", last,  "|", "Full:", full, "|", d['terms'][-1]['type'], d['terms'][-1]['state'])

with open(DATA_FOLDER + "/legislator_ap_mapping.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(['bioguide_id', 'ap_pol_id'])
    writer.writerows(rows)
