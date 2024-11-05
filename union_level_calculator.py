import json
from jobName import union_card_effect_type_cn as ucet, union_card_tier_number_cn as uctn

def ifzero(career_id):
    return int(career_id/100) == 101

def get_level(element):
     return element['level']

def get_union_level(chartable):
    chartable.sort(key=get_level, reverse=True)
    union_level = 0
    character_count = 0
    for i in chartable:
        if character_count == 42:
            break
        else:
            if i['job'] != 0:
                if ifzero(i['job']) and i['level'] < 130:
                    continue
                union_level += i['level']
                character_count += 1
    return union_level

def get_union_effect(job, level):
    if job % 100 == 0 or job % 100 == 1:
        return {}
    else:
        effect = ''
        for i in ucet:
            if job // 10 in ucet[i]:
                effect = i
                break
        if effect == 'SDL':
            result = {'力量': uctn[effect][get_job_tier_key(job, level)], '敏捷': uctn[effect][get_job_tier_key(job, level)], '运气': uctn[effect][get_job_tier_key(job, level)]}
        else:
            try:
                result = {effect: uctn[effect][get_job_tier_key(job, level)]}
            except:
                result = {}
        return result

def get_job_count_key(job, level):
    if ifzero(job):
        if level >= 130 and level < 160:
            tier = 'B'
        elif level >= 160 and level < 180:
            tier = 'A'
        elif level >= 160 and level < 180:
            tier = 'S'
        elif level >= 200 and level < 250:
            tier = 'SS'
        elif level >= 250:
            tier = 'SSS'
        else:
            tier = 'C'
    elif job != 0:
        if level >= 60 and level < 99:
            tier = 'B'
        elif level >= 100 and level < 140:
            tier = 'A'
        elif level >= 140 and level < 200:
            tier = 'S'
        elif level >= 200 and level < 250:
            tier = 'SS'
        elif level >= 250:
            tier = 'SSS'
        else:
            tier = 'C'
    else:
        tier = 'C'
    class_branch = (job - job // 1000 * 1000) // 100
    if class_branch == 7:
        class_branch = 3
    if tier in ['C', 'B', 'A']:
        return tier
    elif tier == 'S':
        if class_branch in [1, 5]:
            return tier + '15'
        else:
            return tier + '234'
    elif tier == 'SS':
        if class_branch == 6:
            return tier + '4'
        else:
            return tier + str(class_branch)
    elif tier == 'SSS':
        return tier + str(class_branch)
    else:
        return 'C'

def get_job_tier_key(job, level):
    if ifzero(job):
        if level >= 130 and level < 160:
            tier = 1
        elif level >= 160 and level < 180:
            tier = 2
        elif level >= 160 and level < 180:
            tier = 3
        elif level >= 200 and level < 250:
            tier = 4
        elif level >= 250:
            tier = 5
        else:
            tier = 0
    elif job % 100 != 0 and job % 100 != 1:
        if level >= 60 and level < 99:
            tier = 1
        elif level >= 100 and level < 140:
            tier = 2
        elif level >= 140 and level < 200:
            tier = 3
        elif level >= 200 and level < 250:
            tier = 4
        elif level >= 250:
            tier = 5
        else:
            tier = 0
    else:
        tier = 0
    return tier

def max_legion_member_quantity(legion_level):
    if legion_level < 1000:
        return 9
    elif 1000 <= legion_level < 1500:
        return 10
    elif 1500 <= legion_level < 2000:
        return 11
    elif 2000 <= legion_level < 2500:
        return 12
    elif 2500 <= legion_level < 3000:
        return 13
    elif 3000 <= legion_level < 3500:
        return 18
    elif 3500 <= legion_level < 4000:
        return 19
    elif 4000 <= legion_level < 4500:
        return 20
    elif 4500 <= legion_level < 5000:
        return 21
    elif 5000 <= legion_level < 5500:
        return 22
    elif 5500 <= legion_level < 6000:
        return 27
    elif 6000 <= legion_level < 6500:
        return 28
    elif 6500 <= legion_level < 7000:
        return 29
    elif 7000 <= legion_level < 7500:
        return 30
    elif 7500 <= legion_level < 8000:
        return 31
    elif 8000 <= legion_level < 8500:
        return 36
    elif 8500 <= legion_level < 9000:
        return 37
    elif 9000 <= legion_level < 9500:
        return 38
    elif 9500 <= legion_level < 1000:
        return 39
    elif 10000 <= legion_level < 10500:
        return 40
    elif 10500 <= legion_level < 11000:
        return 41
    elif 11000 <= legion_level < 11500:
        return 42
    elif 11500 <= legion_level < 12000:
        return 43
    elif 12000 <= legion_level < 12500:
        return 44
    elif 12500 <= legion_level:
        return 45

def get_usable_grid_dict(chartable:list, isAbyssalExpeditionMinarObtained:bool=False, isAbyssalExpeditionElNathObtained:bool=False, isKMSM:bool=False, isCMS:bool=False):
    job_count = {
        'C': 0,
        'B': 0,
        'A': 0,
        'S15': 0,
        'S234': 0,
        'SS1': 0,
        'SS3': 0,
        'SS4': 0,
        'SS2': 0,
        'SS5': 0,
        'SSS1': 0,
        'SSS3': 0,
        'SSS4': 0,
        'SSS2': 0,
        'SSS5': 0,
        'SSS6': 0
    }
    chartable.sort(key=get_level, reverse=True)
    for i in chartable:
        job_count[get_job_count_key(i['job'], i['level'])] += 1
    if isAbyssalExpeditionMinarObtained:
        if isCMS:
            job_count['SS3'] += 1
        else:
            job_count['SSS5'] += 1
    if isAbyssalExpeditionElNathObtained:
        if isCMS:
            job_count['SS5'] += 1
        else:
            job_count['SSS3'] += 1
    if isKMSM:
        job_count['SS3'] += 1
    return job_count


