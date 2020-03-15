from users.models import Data

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

def DataReport(dt):
    context = {}
    data = Data.objects.filter(dt__day=dt.day, dt__month=dt.month, dt__year=dt.year).order_by("-dt")
    context["data"] = data
    context["rej"] = data.filter(status=0).count()
    passed = data.filter(status=1).count()
    context["passed"] = passed
    context["f_arc"] = data.filter(arc=0).count()
    context["f_cont"] = data.filter(cont=0).count()
    context["f_hold"] = data.filter(hold=0).count()
    context["f_trip"] = data.filter(trip=0).count()
    context["f_knr"] = data.filter(knr=0).count()
    context["f_hv"] = data.filter(hv=0).count()
    context["rej_rate"] = "{0:.2f}".format(context["rej"]*100/len(data))
    context["pass_rate"] = "{0:.2f}".format(context["passed"]*100/len(data))
    return context