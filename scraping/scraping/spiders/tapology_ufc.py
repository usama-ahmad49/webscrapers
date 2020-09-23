"""
This file combines data that is scraped from ufc.com and tapology.com and generate a csv file final.csv
"""

import copy
import csv
import json

csv_columns = ['name', 'Date', 'Location', 'ref', 'Fighter 1', 'Fighter 2', 'Red Corner', 'Blue Corner', '1_Odds', '2_Odds',
               'Winner', 'method victory', 'fight length sec.', '1_total strikes att', '1_total strikes ldd',
               '1_sig. strikes att', '1_sig. strikes ldd', '1_takedowns att', '1_takedowns ldd', '1_KD', '1_sub att',
               '1_pass', '1_rev.', '1_sig. strikes head', '1_sig. strikes body', '1_sig. strikes legs',
               '1_sig. strikes distance', '1_sig. strikes clinch', '1_sig. strikes ground', '1_weigh in lbs',
               '1_Age in months at fight', '1_height in cm', '1_reach in cm', '1_Stance', '1_Gym', '1_Nationality',
               '2_total strikes att', '2_total strikes ldd', '2_sig. strikes att', '2_sig. strikes ldd',
               '2_takedowns att', '2_takedowns ldd', '2_KD', '2_sub att', '2_pass', '2_rev.', '2_sig. strikes head',
               '2_sig. strikes body', '2_sig. strikes legs', '2_sig. strikes distance', '2_sig. strikes clinch',
               '2_sig. strikes ground', '2_weigh in lbs', '2_Age in months at fight', '2_height in cm', '2_reach in cm',
               '2_Stance', '2_Gym', '2_Nationality', 'number of rounds', 'championship fight', '1_pro record at fight',
               '2_pro record at fight', 'weightclass', 'event']
csvfile = open('final.csv', 'w', newline='', encoding="utf-8")
writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
writer.writeheader()


def get_ufc_data():
    file = open("ufc_com.txt", "r")
    ufc_fights = []
    for line in file:
        ufc_fights.append(json.loads(line))
    return ufc_fights


def get_tapology_data():
    input_file = csv.DictReader(open("tapology.csv", encoding="utf-8"))
    tapology_fights = []
    for row in input_file:
        tapology_fights.append(row)
    return tapology_fights


def get_dict_value(data, key_list, default='NULL'):
        """
        gets a dictionary and key_list, apply key_list sequentially on dictionary and return value
        :param data: dictionary
        :param key_list: list of key
        :param default: return value if key not found
        :return:
        """
        for key in key_list:
            if data and isinstance(data, dict):
                data = data.get(key, default)
            else:
                return default
        return data if data else 'NULL'


def get_strikes(data, color, key1, key2):

    if data['FMLiveFeed']['FightCard']['Fight'][2]['FightStats'][0]['Color'].lower() == color:
        all_strikes = get_dict_value(data, ['FMLiveFeed', 'FightCard', 'Fight'])[2]['FightStats'][0]['Fighter'][0]['Strikes']
    else:
        all_strikes = get_dict_value(data, ['FMLiveFeed', 'FightCard', 'Fight'])[2]['FightStats'][1]['Fighter'][0][
            'Strikes']
    for strike in all_strikes:
        if strike['Name'] == key1:
            return strike.get(key2)


def get_grappling(data, color, key1, key2):
    if data['FMLiveFeed']['FightCard']['Fight'][2]['FightStats'][0]['Color'].lower() == color:
        all_strikes = get_dict_value(data, ['FMLiveFeed', 'FightCard', 'Fight'])[2]['FightStats'][0]['Fighter'][1]['Grappling']
    else:
        all_strikes = get_dict_value(data, ['FMLiveFeed', 'FightCard', 'Fight'])[2]['FightStats'][1]['Fighter'][1][
            'Grappling']
    for strike in all_strikes:
        if strike['Name'] == key1:
            return strike.get(key2)


def combine_data(ufc_fights, tapology_fights):
    ufc_fights.reverse()
    for ufc_fight in ufc_fights:
        data = ufc_fight['api_data']
        item = dict()
        item.update(ufc_fight['scraped_item'])
        item['name'] = item['name'].strip()
        item['Date'] = ufc_fight['event_date']
        try:
            fight_time = data['FMLiveFeed'].get('CurrentRoundTime', '').split(':')
            item['fight length sec.'] = (int(fight_time[0])*60) + int(fight_time[1])
        except:
            item['fight length sec.'] = ''
        item['ref'] = data['FMLiveFeed'].get('Referee') or get_dict_value(data, ['FMLiveFeed', 'FightCard', 'Referee'])

        item['1_total strikes att'] = get_dict_value(data, ['FMLiveFeed', 'FightStats', 'Red', 'Strikes',
                                                            'Total Strikes', 'Attempts'
                                                            ]) or get_strikes(data, 'red', 'Total Strikes', 'Attempts')
        item['1_total strikes ldd'] = get_dict_value(data, ['FMLiveFeed', 'FightStats', 'Red', 'Strikes',
                                                            'Total Strikes', 'Landed'
                                                            ]) or get_strikes(data, 'red', 'Total Strikes', 'Landed')
        item['1_sig. strikes att'] = get_dict_value(data, ['FMLiveFeed', 'FightStats', 'Red', 'Strikes',
                                                           'Significant Strikes', 'Attempts'
                                                           ]) or get_strikes(data, 'red', 'Significant Strikes', 'Attempts')
        item['1_sig. strikes ldd'] = get_dict_value(data, ['FMLiveFeed', 'FightStats', 'Red', 'Strikes',
                                                           'Significant Strikes', 'Landed'
                                                           ]) or get_strikes(data, 'red', 'Significant Strikes', 'Landed')
        item['1_takedowns att'] = get_dict_value(data, ['FMLiveFeed', 'FightStats', 'Red', 'Grappling', 'Takedowns',
                                                        'Attempts']) or get_grappling(data, 'red', 'Takedowns',
                                                                                      'Attempts')
        item['1_takedowns ldd'] = get_dict_value(data, ['FMLiveFeed', 'FightStats', 'Red', 'Grappling', 'Takedowns',
                                                        'Landed']) or get_grappling(data, 'red', 'Takedowns',
                                                                                      'Success')
        item['1_KD'] = get_dict_value(data, ['FMLiveFeed', 'FightStats', 'Red', 'Strikes', 'Knock Down', 'Landed'
                                             ]) or get_strikes(data, 'red', 'Knock down', 'Landed')
        item['1_sub att'] = get_dict_value(data, ['FMLiveFeed', 'FightStats', 'Red', 'Grappling', 'Submissions',
                                                  'Attempts']) or get_grappling(data, 'red', 'Submissions', 'Success')
        item['1_pass'] = get_dict_value(data, ['FMLiveFeed', 'FightStats', 'Red', 'Grappling', 'Standups', 'Landed'
                                               ]) or get_grappling(data, 'red', 'Standups', 'Success')
        item['1_rev.'] = get_dict_value(data, ['FMLiveFeed', 'FightStats', 'Red', 'Grappling', 'Reversals', 'Landed'
                                               ]) or get_grappling(data, 'red', 'Reversals', 'Success')
        item['1_sig. strikes head'] = get_dict_value(data, ['FMLiveFeed', 'FightStats', 'Red', 'Strikes',
                                                            'Head Significant Strikes', 'Landed'
                                                            ]) or get_strikes(data, 'red', 'Head Significant Strikes',
                                                                              'Landed')
        item['1_sig. strikes body'] = get_dict_value(data, ['FMLiveFeed', 'FightStats', 'Red', 'Strikes',
                                                            'Body Significant Strikes', 'Landed'
                                                            ]) or get_strikes(data, 'red', 'Body Significant Strikes',
                                                                              'Landed')
        item['1_sig. strikes legs'] = get_dict_value(data, ['FMLiveFeed', 'FightStats', 'Red', 'Strikes',
                                                            'Legs Significant Strikes', 'Landed'
                                                            ]) or get_strikes(data, 'red', 'Legs Significant Strikes',
                                                                              'Landed')
        item['1_sig. strikes distance'] = get_dict_value(data, ['FMLiveFeed', 'FightStats', 'Red', 'Strikes',
                                                            'Distance Strikes', 'Landed'
                                                            ]) or get_strikes(data, 'red', 'Distance Strikes',
                                                                              'Landed')
        item['1_sig. strikes clinch'] = get_dict_value(data, ['FMLiveFeed', 'FightStats', 'Red', 'Strikes',
                                                              'Clinch Total Strikes', 'Landed'
                                                              ]) or get_strikes(data, 'red', 'Clinch Total Strikes ',
                                                                              'Landed')
        item['1_sig. strikes ground'] = get_dict_value(data, ['FMLiveFeed', 'FightStats', 'Red', 'Strikes',
                                                              'Ground Total Strikes', 'Landed'
                                                              ]) or get_strikes(data, 'red', 'Ground Total Strikes ',
                                                                              'Landed')




        item['2_total strikes att'] = get_dict_value(data, ['FMLiveFeed', 'FightStats', 'Blue', 'Strikes',
                                                            'Total Strikes', 'Attempts'
                                                            ]) or get_strikes(data, 'blue', 'Total Strikes', 'Attempts')
        item['2_total strikes ldd'] = get_dict_value(data, ['FMLiveFeed', 'FightStats', 'Blue', 'Strikes',
                                                            'Total Strikes', 'Landed'
                                                            ]) or get_strikes(data, 'blue', 'Total Strikes', 'Landed')
        item['2_sig. strikes att'] = get_dict_value(data, ['FMLiveFeed', 'FightStats', 'Blue', 'Strikes',
                                                           'Significant Strikes', 'Attempts'
                                                           ]) or get_strikes(data, 'blue', 'Significant Strikes', 'Attempts')
        item['2_sig. strikes ldd'] = get_dict_value(data, ['FMLiveFeed', 'FightStats', 'Blue', 'Strikes',
                                                           'Significant Strikes', 'Landed'
                                                           ]) or get_strikes(data, 'blue', 'Significant Strikes', 'Landed')
        item['2_takedowns att'] = get_dict_value(data, ['FMLiveFeed', 'FightStats', 'Blue', 'Grappling', 'Takedowns',
                                                        'Attempts']) or get_grappling(data, 'red', 'Takedowns',
                                                                                      'Attempts')
        item['2_takedowns ldd'] = get_dict_value(data, ['FMLiveFeed', 'FightStats', 'Blue', 'Grappling', 'Takedowns',
                                                        'Landed']) or get_grappling(data, 'blue', 'Takedowns',
                                                                                      'Success')
        item['2_KD'] = get_dict_value(data, ['FMLiveFeed', 'FightStats', 'Blue', 'Strikes', 'Knock Down', 'Landed'
                                             ]) or get_strikes(data, 'blue', 'Knock down', 'Landed')
        item['2_sub att'] = get_dict_value(data, ['FMLiveFeed', 'FightStats', 'Blue', 'Grappling', 'Submissions',
                                                  'Attempts']) or get_grappling(data, 'blue', 'Submissions', 'Success')
        item['2_pass'] = get_dict_value(data, ['FMLiveFeed', 'FightStats', 'Blue', 'Grappling', 'Standups', 'Landed'
                                               ]) or get_grappling(data, 'blue', 'Standups', 'Success')
        item['2_rev.'] = get_dict_value(data, ['FMLiveFeed', 'FightStats', 'Blue', 'Grappling', 'Reversals', 'Landed'
                                               ]) or get_grappling(data, 'blue', 'Reversals', 'Success')
        item['2_sig. strikes head'] = get_dict_value(data, ['FMLiveFeed', 'FightStats', 'Blue', 'Strikes',
                                                            'Head Significant Strikes', 'Landed'
                                                            ]) or get_strikes(data, 'blue', 'Head Significant Strikes',
                                                                              'Landed')
        item['2_sig. strikes body'] = get_dict_value(data, ['FMLiveFeed', 'FightStats', 'Blue', 'Strikes',
                                                            'Body Significant Strikes', 'Landed'
                                                            ]) or get_strikes(data, 'blue', 'Body Significant Strikes',
                                                                              'Landed')
        item['2_sig. strikes legs'] = get_dict_value(data, ['FMLiveFeed', 'FightStats', 'Blue', 'Strikes',
                                                            'Legs Significant Strikes', 'Landed'
                                                            ]) or get_strikes(data, 'blue', 'Legs Significant Strikes',
                                                                              'Landed')
        item['2_sig. strikes distance'] = get_dict_value(data, ['FMLiveFeed', 'FightStats', 'Blue', 'Strikes',
                                                            'Distance Strikes', 'Landed'
                                                            ]) or get_strikes(data, 'blue', 'Distance Strikes',
                                                                              'Landed')
        item['2_sig. strikes clinch'] = get_dict_value(data, ['FMLiveFeed', 'FightStats', 'Blue', 'Strikes',
                                                              'Clinch Total Strikes', 'Landed'
                                                              ]) or get_strikes(data, 'blue', 'Clinch Total Strikes ',
                                                                              'Landed')
        item['2_sig. strikes ground'] = get_dict_value(data, ['FMLiveFeed', 'FightStats', 'Blue', 'Strikes',
                                                              'Ground Total Strikes', 'Landed'
                                                              ]) or get_strikes(data, 'blue', 'Ground Total Strikes ',
                                                                              'Landed')
        item['number of rounds'] = data['FMLiveFeed'].get('CurrentRound') or data['FMLiveFeed']['FightCard']['CurRound']
        item['weightclass'] = data['FMLiveFeed'].get('WeightClass') or get_dict_value(data, ['FMLiveFeed', 'FightCard',
                                                                                             'WeightClass'])
        found = False
        for tapology_fight in tapology_fights:
            if item['Date'] == tapology_fight['date'] and item['name'] == tapology_fight['name_on_ufc']:
                item['Location'] = tapology_fight['Location']
                item['event'] = tapology_fight['event']
                found = True
                if item['Fighter 1'].strip() == tapology_fight['left_fighter'].strip():
                    item['1_pro record at fight'] = tapology_fight['left_pro_record']
                    item['2_pro record at fight'] = tapology_fight['right_pro_record']
                    item['1_Odds'] = tapology_fight['left_odds']
                    item['2_Odds'] = tapology_fight['right_odds']
                    item['1_Gym'] = tapology_fight['left_gym']
                    item['2_Gym'] = tapology_fight['right_gym']
                    item['1_Nationality'] = tapology_fight['left_nationality']
                    item['2_Nationality'] = tapology_fight['right_nationality']
                    item['1_weigh in lbs'] = tapology_fight['left_weight']
                    item['2_weigh in lbs'] = tapology_fight['right_weight']
                    item['1_Age in months at fight'] = tapology_fight['left_age']
                    item['2_Age in months at fight'] = tapology_fight['right_age']
                    item['1_height in cm'] = tapology_fight['left_height']
                    item['2_height in cm'] = tapology_fight['right_height']
                    item['1_reach in cm'] = tapology_fight['left_reach']
                    item['2_reach in cm'] = tapology_fight['right_reach']
                else:
                    item['2_pro record at fight'] = tapology_fight['left_pro_record']
                    item['1_pro record at fight'] = tapology_fight['right_pro_record']
                    item['2_Odds'] = tapology_fight['left_odds']
                    item['1_Odds'] = tapology_fight['right_odds']
                    item['2_Gym'] = tapology_fight['left_gym']
                    item['1_Gym'] = tapology_fight['right_gym']
                    item['2_Nationality'] = tapology_fight['left_nationality']
                    item['1_Nationality'] = tapology_fight['right_nationality']
                    item['2_weigh in lbs'] = tapology_fight['left_weight']
                    item['1_weigh in lbs'] = tapology_fight['right_weight']
                    item['2_Age in months at fight'] = tapology_fight['left_age']
                    item['1_Age in months at fight'] = tapology_fight['right_age']
                    item['2_height in cm'] = tapology_fight['left_height']
                    item['1_height in cm'] = tapology_fight['right_height']
                    item['2_reach in cm'] = tapology_fight['left_reach']
                    item['1_reach in cm'] = tapology_fight['right_reach']
                writer.writerow(item)
        if not found:
            print('{} : {} : {} : {}'.format(item['name'], item['Date'], item['Fighter 1'], item['Fighter 2']))


if __name__ == '__main__':
    ufc_fights = get_ufc_data()
    tapology_fights = get_tapology_data()
    combined_data = combine_data(ufc_fights, tapology_fights)
