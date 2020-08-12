from users.models import Machine

def getMachine(request):
  m = Machine.objects.all()
  print("m is ",m)
  if len(m) == 1:
    return {'machine': m[0].machine, 'line': m[0].line}
  return {}