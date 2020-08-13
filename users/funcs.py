from users.models import *
from datetime import datetime, timedelta
from django.db.models import Q, Count

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

def DataReport(dt, query=False, data=None):
    context = {}
    if not query:
        data = QueryDate(dt)
        if len(data) == 0:
            return {}
    context["data"] = data
    context["rej"] = data.filter(status=0).count()
    context["passed"] = data.filter(status=1).count()
    context["f_arc"] = data.filter(arc=0).count()
    context["f_cont"] = data.filter(cont=0).count()
    context["f_hold"] = data.filter(hold=0).count()
    context["f_trip"] = data.filter(trip=0).count()
    context["f_knr"] = data.filter(knr=0).count()
    context["f_hv"] = data.filter(hv=0).count()
    context["rej_rate"] = "{0:.2f}".format(context["rej"]*100/len(data))
    context["pass_rate"] = "{0:.2f}".format(context["passed"]*100/len(data))
    context['tcount'] = len(data)
    context['count'] = len(data)-len(context['data'])
    return context

def QueryDate(dt, edt=None):
    next_dt = dt+timedelta(days=1)
    # return Data.objects.filter(dt__day=dt.day, dt__month=dt.month, dt__year=dt.year)
    print("dt, ",dt, "edt ", edt)
    if edt:
        # return Data.objects.filter(dt__year=dt.year, dt__month=dt.month, dt__day__gte=dt.day, dt__day__lte=edt.day \
        #     , Q(dt__hour__gte=dt.hour)&Q(dt__hour__lte=edt.hour), Q(dt__minute__gte=dt.minute)&Q(dt__minute__lte=edt.minute))
        return Data.objects.filter(dt__gte=dt, dt__lte=edt)
    st = ShiftTime.objects.filter().first()
    return Data.objects.filter(Q(dt__gte="{} {}:00:00".format(dt.date(), st.From))&Q(dt__lte="{} {}:59:59".format(next_dt.date(), st.to-1)))

def RatingReport(dt, edt=None):
    qdt = QueryDate(dt, edt)
    if not qdt:
        return {}
    d = {}
    data = qdt.values("rating").annotate(Count("rating"))
    for i in data:
        i["report"] = DataReport(dt, query=True, data=qdt.filter(rating=i["rating"]))
        i["report"].pop("data")
    d["total"] = DataReport(dt, query=True, data=qdt)
    d["total"].pop("data")
    d["data"] = qdt
    d["report"] = data
    d["dt"] = dt
    if not edt:
        d["edt"] = dt + timedelta(days=1)
    return d