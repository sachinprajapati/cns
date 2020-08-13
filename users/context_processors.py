from users.models import Machine

def getMachine(request):
  m = Machine.objects.filter()
  if len(m) == 1:
    return {'machine': m[0].get_machine_display(), 'line': m[0].line}
  return {}