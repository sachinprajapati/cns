st = "RC32.0HOLDV 90HOLDP0TRIPV182TRIPP0KNRP0HVP0OVER0HI   0.0TI   0.0HT   0TT   0CO0AC0$00"
st1 = "RC 6.0HOLDV 83HOLDP1TRIPV151TRIPP1KNRP1HVP1OVER1HI  33.1TI  59.8HT 103TT  14CO1AC1$00"
st2 = "RC 6.0HOLDV 83HOLDP1TRIPV151TRIPP1KNRP1HVP1OVER1HI  33.1TI  59.8HT 103TT  14CO0AC1$00"

def Exact(st):
    d = {}
    d["rating"] = float(st[2:6].strip()) #R
    d["hold_v"] = float(st[11:14].strip()) #HOLDV
    d["trip_v"] = float(st[25:28].strip()) #TRIPV
    d["hold_a"] = float(st[50:56].strip()) #HI
    d["trip_a"] = float(st[58:64].strip()) #TI
    d["hold_t"] = float(st[66:70].strip()) #HT
    d["trip_t"] = float(st[72:76].strip()) #TT
    if st[81] == '1':
        d['arc'] = 1
        if st[78] == '1':
            d['cont'] = 1
            if st[18:20] == 'P1':
                d['hold'] = 1
                if st[32:34] == 'P1':
                    d['trip'] = 1
                    if st[37:39] == 'P1':
                        d["knr"] = 1
                        if st[41:43] == 'P1':
                            d['hv'] = 1
                            if st[47] == '1':
                                d['status'] = 1
                        elif st[41:43] == 'P0':
                            d['hv'] = 0

                    elif st[37:39] == 'P0':
                        d['knr'] = 0
                elif st[32:34] == 'P0':
                    d['trip'] = 0
            elif st[18:20] == 'P0':
                d['hold'] = 0
        elif st[78] == '0':
            d['cont'] = 0
    return d
