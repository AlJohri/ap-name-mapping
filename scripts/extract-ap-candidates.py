#!/usr/bin/env python3

import os
import sys
import csv
import json

DATA_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')

candidates = {}

polid_blacklist = ['0']

for filename in os.listdir(DATA_FOLDER + "/raw_ap/"):
# filenames = ["2012-11-06.json", "2015-11-03.json", "2015-11-21.json", "2016-11-08.json"]
# for filename in filenames:
    with open(DATA_FOLDER + "/raw_ap/" + filename) as f:
        data = json.load(f)
        for race in data['races']:

            if race['officeID'] not in ['H', 'S', 'G', 'P']: continue
            if race['raceTypeID'] not in ['G']: continue

            state_reporting_unit = [x for x in race['reportingUnits'] if x['level'] in ['state', 'national']][0]

            for candidate in state_reporting_unit['candidates']:
                election_date = filename.replace(".json", "")
                if candidate['polID'] in polid_blacklist: continue
                candidates[(
                    election_date,
                    race['raceID'],
                    race.get('raceType', ''),
                    race['officeName'],
                    state_reporting_unit.get('statePostal'),
                    state_reporting_unit.get('seatNum'),
                    state_reporting_unit.get('seatName'),
                    candidate['candidateID']
                )] = candidate

rows = []
for (election_date, race_id, race_type, office_name, state_postal, seat_num, seat_name, candidate_id), candidate in candidates.items():
    row = {
        'election_date': election_date,
        'pol_id': candidate.get('polID'),
        'cand_id': int(candidate_id),
        'race_id': int(race_id),
        'race_type': race_type,
        'office_name': office_name,
        'state_postal': state_postal,
        'seat_num': seat_num,
        'seat_name': seat_name,
        'first_name': candidate.get('first', ''),
        'middle_name': candidate.get('middle', ''),
        'last_name': candidate['last'],
        'suffix': candidate.get('suffix', ''),
        'abbrv': candidate.get('abbrv', ''),
        'party': candidate.get('party', '')
    }
    rows.append(row)
rows.sort(key=lambda x: (x['pol_id'], x['election_date'], x['cand_id'], x['race_id']))
with open(DATA_FOLDER + "/ap_candidates.csv", "w") as f:
    writer = csv.DictWriter(f, fieldnames=['pol_id', 'election_date', 'cand_id', 'race_id', 'race_type', 'office_name', 'state_postal', 'seat_num', 'seat_name', 'first_name', 'middle_name', 'last_name', 'suffix', 'abbrv', 'party'])
    writer.writeheader()
    writer.writerows(rows)

# pols = [1829, 1968, 7623, 7877, 8639, 11076, 11291, 28400, 32985, 34467, 40662, 45650, 57706, 57725, 58194, 59729, 61428, 61504, 61911, 62535, 63153, 64541, 64546, 64547, 64548, 64549, 64550, 64551, 64552, 64553, 64554, 64555, 64556, 64557, 64558, 64559, 64560, 64561, 64562, 64563, 64564, 64565, 64566, 64567, 64569, 64576, 64577, 64659, 64660, 64722, 64723, 64724, 64725, 64726, 64727, 64750, 64751, 64868, 64879, 64975, 64976, 64977, 64978, 64979, 64980, 64981, 64982, 64983, 65100]
# for x in pols: Politician.objects.get(ap_id=x).delete()
