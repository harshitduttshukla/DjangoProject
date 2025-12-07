@active(detail=True,method=['post'],url_path='resolve')
def resolve(self,request,pk=None):
    case = self.get_object()
    case.status = 'resolved'
    case.resolved_at = timezone.now()
    case.resolution_notes = request.data.get('resolution_notes','')
    case.save()
    return Response(CaseSerial(case).data)


class