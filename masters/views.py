from .models import DBPMaster, AuditTrails,DAPMaster,TMFMaster,WCMaster
from .serializers import (
    DBPModelSerializer, NestedDBPModelSerializer, PostDBPSerializer,
    PatchDBPSerializer,DayGetRequest,AuditTrailsSerializer,
    AuditTrailRequestSerializer, NestedAuditTrailsSerializer,
    DAPModelSerializer,PostDAPSerializer,PatchDAPSerializer,NestedDAPModelSerializer,
    PatchTMFSerializer,PostTMFSerializer,TMFModelSerializer,NestedTMFModelSerializer,
    PostWCSerializer,PatchWCSerializer,WCModelSerializer,NestedWCModelSerializer,
    CalculationsRequestSerializer)
from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK,HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_422_UNPROCESSABLE_ENTITY
from traceback import format_exc
from drf_spectacular.utils import extend_schema
from django.db.transaction import atomic
from datetime import datetime
# Create your views here.


@extend_schema(tags=["DBP View"])
class DBPView(APIView):    
    def get(self,request):
        try:
            _id = request.GET.get('id')
            if _id is None:
                _dbp_master = DBPMaster.objects.select_related('created_by','updated_by').all()
                _serialized_dbp = NestedDBPModelSerializer(_dbp_master,many=True)
                return Response({
                    'message':"Successfully fetched data",
                    'data':_serialized_dbp.data
                },status=HTTP_200_OK)
            else:
                _dbp_master = DBPMaster.objects.filter(id=_id).last()
                if _dbp_master is None:
                    return Response(status=HTTP_404_NOT_FOUND,data={
                        'message':f"Cannot fetch data with id={_id}"
                    })
                else:
                    _serialized_dbp = NestedDBPModelSerializer(_dbp_master)
                    return Response({
                        'message':"Successfully fetched data",
                        'data':_serialized_dbp.data
                    },status=HTTP_200_OK)
        except Exception as ex:
            print(f'Failed to execute the API')
            print(format_exc(ex))
            return APIException(detail={
                    'message':'Something went wrong'
                }, code=HTTP_500_INTERNAL_SERVER_ERROR)
    
    @extend_schema(request=PostDBPSerializer)
    @atomic
    def post(self,request):
        try:
            _request = PostDBPSerializer(data={**request.data})
            if not _request.is_valid():
                return Response({
                    'message':"Invalid Request",
                    'errors':_request.errors
                },status=HTTP_422_UNPROCESSABLE_ENTITY)
            
            _model_serializer = DBPModelSerializer(data={**request.data,'created_by':request.user.id})
            
            if _model_serializer.is_valid(raise_exception=True):
                _model_serializer.save()
                _trail = AuditTrailsSerializer(data={
                    'audit_type':'DBP',
                    'tx_id':_model_serializer.data['id'],
                    'data':_model_serializer.data,
                    'created_by':request.user.id
                })
                if _trail.is_valid(raise_exception=True):
                    _trail.save()
                return Response({
                    'message':"Successfully saved data",
                    'data':_model_serializer.data
                },status=HTTP_201_CREATED)
            
            
        except Exception as ex:
            print(f'Failed to execute the API')
            print(format_exc(ex))
            raise APIException(detail={
                    'message':'Something went wrong'
                }, code=HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(request=PatchDBPSerializer)
    @atomic
    def patch(self,request):
        try:
            _request = PatchDBPSerializer(data={**request.data})
            if not _request.is_valid():
                return Response({
                    'message':"Invalid Request",
                    'errors':_request.errors
                },status=HTTP_422_UNPROCESSABLE_ENTITY)
            
            _id = _request.data['id']
            
            _dbp_model = DBPMaster.objects.filter(id=_id).last()
            
            if _dbp_model is None:
                return Response(status=HTTP_404_NOT_FOUND,data={
                    'message':f"Cannot fetch data with id={_id}"
                })
            
            
            
            _model_serializer = DBPModelSerializer(_dbp_model,data={**_request.data,'created_by':request.user.id})
            
            if _model_serializer.is_valid(raise_exception=True):
                _model_serializer.save()
                _trail = AuditTrailsSerializer(data={
                    'audit_type':'DBP',
                    'tx_id':_model_serializer.data['id'],
                    'data':_model_serializer.data,
                    'created_by':request.user.id
                })
                if _trail.is_valid(raise_exception=True):
                    _trail.save()
                return Response({
                    'message':"Successfully saved data",
                    'data':_model_serializer.data
                },status=HTTP_201_CREATED)
            
            
        except Exception as ex:
            print(f'Failed to execute the API')
            print(format_exc(ex))
            raise APIException(detail={
                    'message':'Something went wrong'
                }, code=HTTP_500_INTERNAL_SERVER_ERROR)


DAYS = [
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
]


@extend_schema(tags=["Day Dropdown View"])
class DayDropdown(APIView):
    @extend_schema(parameters=[DayGetRequest])
    def get(self,request):
        try:
            dbp_id = request.GET.get('dbp_id')
            used_dates = list(DBPMaster.objects.values_list('applicable_days',flat=True))
            _used_dates = []
            for i in used_dates:
                for j in i:
                    _used_dates.append(j)
            used_dates = _used_dates
            if dbp_id is None:
                _availaible_dates = [i for i in DAYS if i not in used_dates]
                
            else:
                days = list(set(DBPMaster.objects.filter(id=dbp_id).values_list('applicable_days',flat=True).first()))
                _availaible_dates = [i for i in DAYS if i not in used_dates or i in days]
            
            return Response({
                'message':"Successfully saved data",
                'data':_availaible_dates
            },status=HTTP_201_CREATED)
                
        except Exception as ex:
            print(f'Failed to execute the API')
            print(format_exc(ex))
            return APIException(detail={
                    'message':'Something went wrong'
                }, code=HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(tags=["Audit trail View"])
class AuditTrailView(APIView):
    @extend_schema(parameters=[AuditTrailRequestSerializer])
    def get(self,request):
        try:
            audit_tx_id = request.GET.get('audit_tx_id')
            audit_type = request.GET.get('audit_type')
            _audits = AuditTrails.objects.filter(tx_id=audit_tx_id,audit_type=audit_type)
            _serialized_audit = NestedAuditTrailsSerializer(_audits,many=True)
            return Response({
                    'message':"Successfully fetched data",
                    'data':_serialized_audit.data
                },status=HTTP_200_OK)
        except Exception as ex:
            print(f'Failed to execute the API')
            print(format_exc(ex))
            return APIException(detail={
                    'message':'Something went wrong'
                }, code=HTTP_500_INTERNAL_SERVER_ERROR)



@extend_schema(tags=["DAP View"])
class DAPView(APIView):    
    def get(self,request):
        try:
            _id = request.GET.get('id')
            if _id is None:
                _dap_master = DAPMaster.objects.select_related('created_by','updated_by').all()
                _serialized_dap = NestedDAPModelSerializer(_dap_master,many=True)
                return Response({
                    'message':"Successfully fetched data",
                    'data':_serialized_dap.data
                },status=HTTP_200_OK)
            else:
                _dap_master = DAPMaster.objects.filter(id=_id).last()
                if _dap_master is None:
                    return Response(status=HTTP_404_NOT_FOUND,data={
                        'message':f"Cannot fetch data with id={_id}"
                    })
                else:
                    _serialized_dap = NestedDAPModelSerializer(_dap_master)
                    return Response({
                        'message':"Successfully fetched data",
                        'data':_serialized_dap.data
                    },status=HTTP_200_OK)
        except Exception as ex:
            print(f'Failed to execute the API')
            print(format_exc(ex))
            return APIException(detail={
                    'message':'Something went wrong'
                }, code=HTTP_500_INTERNAL_SERVER_ERROR)
    
    @extend_schema(request=PostDAPSerializer)
    @atomic
    def post(self,request):
        try:
            _request = PostDAPSerializer(data={**request.data})
            if not _request.is_valid():
                return Response({
                    'message':"Invalid Request",
                    'errors':_request.errors
                },status=HTTP_422_UNPROCESSABLE_ENTITY)
            
            _model_serializer = DAPModelSerializer(data={**request.data,'created_by':request.user.id})
            
            if _model_serializer.is_valid(raise_exception=True):
                _model_serializer.save()
                _trail = AuditTrailsSerializer(data={
                    'audit_type':'DAP',
                    'tx_id':_model_serializer.data['id'],
                    'data':_model_serializer.data,
                    'created_by':request.user.id
                })
                if _trail.is_valid(raise_exception=True):
                    _trail.save()
                return Response({
                    'message':"Successfully saved data",
                    'data':_model_serializer.data
                },status=HTTP_201_CREATED)
            
            
        except Exception as ex:
            print(f'Failed to execute the API')
            print(format_exc(ex))
            raise APIException(detail={
                    'message':'Something went wrong'
                }, code=HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(request=PatchDAPSerializer)
    @atomic
    def patch(self,request):
        try:
            _request = PatchDAPSerializer(data={**request.data})
            if not _request.is_valid():
                return Response({
                    'message':"Invalid Request",
                    'errors':_request.errors
                },status=HTTP_422_UNPROCESSABLE_ENTITY)
            
            _id = _request.data['id']
            
            _dap_model = DAPMaster.objects.filter(id=_id).last()
            
            if _dap_model is None:
                return Response(status=HTTP_404_NOT_FOUND,data={
                    'message':f"Cannot fetch data with id={_id}"
                })
            
            
            
            _model_serializer = DAPModelSerializer(_dap_model,data={**_request.data,'created_by':request.user.id})
            
            if _model_serializer.is_valid(raise_exception=True):
                _model_serializer.save()
                _trail = AuditTrailsSerializer(data={
                    'audit_type':'DAP',
                    'tx_id':_model_serializer.data['id'],
                    'data':_model_serializer.data,
                    'created_by':request.user.id
                })
                if _trail.is_valid(raise_exception=True):
                    _trail.save()
                return Response({
                    'message':"Successfully saved data",
                    'data':_model_serializer.data
                },status=HTTP_201_CREATED)
            
            
        except Exception as ex:
            print(f'Failed to execute the API')
            print(format_exc(ex))
            raise APIException(detail={
                    'message':'Something went wrong'
                }, code=HTTP_500_INTERNAL_SERVER_ERROR)








@extend_schema(tags=["TMF View"])
class TMFView(APIView):    
    def get(self,request):
        try:
            _id = request.GET.get('id')
            if _id is None:
                _tmf_master = TMFMaster.objects.select_related('created_by','updated_by').all()
                _serialized_tmf = NestedTMFModelSerializer(_tmf_master,many=True)
                return Response({
                    'message':"Successfully fetched data",
                    'data':_serialized_tmf.data
                },status=HTTP_200_OK)
            else:
                _tmf_master = TMFMaster.objects.filter(id=_id).last()
                if _tmf_master is None:
                    return Response(status=HTTP_404_NOT_FOUND,data={
                        'message':f"Cannot fetch data with id={_id}"
                    })
                else:
                    _serialized_tmf = NestedTMFModelSerializer(_tmf_master)
                    return Response({
                        'message':"Successfully fetched data",
                        'data':_serialized_tmf.data
                    },status=HTTP_200_OK)
        except Exception as ex:
            print(f'Failed to execute the API')
            print(format_exc(ex))
            return APIException(detail={
                    'message':'Something went wrong'
                }, code=HTTP_500_INTERNAL_SERVER_ERROR)
    
    @extend_schema(request=PostTMFSerializer)
    @atomic
    def post(self,request):
        try:
            _request = PostTMFSerializer(data={**request.data})
            if not _request.is_valid():
                return Response({
                    'message':"Invalid Request",
                    'errors':_request.errors
                },status=HTTP_422_UNPROCESSABLE_ENTITY)
            
            _model_serializer = TMFModelSerializer(data={**request.data,'created_by':request.user.id})
            
            if _model_serializer.is_valid(raise_exception=True):
                _model_serializer.save()
                _trail = AuditTrailsSerializer(data={
                    'audit_type':'TMF',
                    'tx_id':_model_serializer.data['id'],
                    'data':_model_serializer.data,
                    'created_by':request.user.id
                })
                if _trail.is_valid(raise_exception=True):
                    _trail.save()
                return Response({
                    'message':"Successfully saved data",
                    'data':_model_serializer.data
                },status=HTTP_201_CREATED)
            
            
        except Exception as ex:
            print(f'Failed to execute the API')
            print(format_exc(ex))
            raise APIException(detail={
                    'message':'Something went wrong'
                }, code=HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(request=PatchTMFSerializer)
    @atomic
    def patch(self,request):
        try:
            _request = PatchTMFSerializer(data={**request.data})
            if not _request.is_valid():
                return Response({
                    'message':"Invalid Request",
                    'errors':_request.errors
                },status=HTTP_422_UNPROCESSABLE_ENTITY)
            
            _id = _request.data['id']
            
            _tmf_model = TMFMaster.objects.filter(id=_id).last()
            
            if _tmf_model is None:
                return Response(status=HTTP_404_NOT_FOUND,data={
                    'message':f"Cannot fetch data with id={_id}"
                })
            
            
            
            _model_serializer = TMFModelSerializer(_tmf_model,data={**_request.data,'created_by':request.user.id})
            
            if _model_serializer.is_valid(raise_exception=True):
                _model_serializer.save()
                _trail = AuditTrailsSerializer(data={
                    'audit_type':'TMF',
                    'tx_id':_model_serializer.data['id'],
                    'data':_model_serializer.data,
                    'created_by':request.user.id
                })
                if _trail.is_valid(raise_exception=True):
                    _trail.save()
                return Response({
                    'message':"Successfully saved data",
                    'data':_model_serializer.data
                },status=HTTP_201_CREATED)
            
            
        except Exception as ex:
            print(f'Failed to execute the API')
            print(format_exc(ex))
            raise APIException(detail={
                    'message':'Something went wrong'
                }, code=HTTP_500_INTERNAL_SERVER_ERROR)






@extend_schema(tags=["WC View"])
class WCView(APIView):    
    def get(self,request):
        try:
            _id = request.GET.get('id')
            if _id is None:
                _wc_master = WCMaster.objects.select_related('created_by','updated_by').all()
                _serialized_wc = NestedWCModelSerializer(_wc_master,many=True)
                return Response({
                    'message':"Successfully fetched data",
                    'data':_serialized_wc.data
                },status=HTTP_200_OK)
            else:
                _wc_master = WCMaster.objects.filter(id=_id).last()
                if _wc_master is None:
                    return Response(status=HTTP_404_NOT_FOUND,data={
                        'message':f"Cannot fetch data with id={_id}"
                    })
                else:
                    _serialized_wc = NestedWCModelSerializer(_wc_master)
                    return Response({
                        'message':"Successfully fetched data",
                        'data':_serialized_wc.data
                    },status=HTTP_200_OK)
        except Exception as ex:
            print(f'Failed to execute the API')
            print(format_exc(ex))
            return APIException(detail={
                    'message':'Something went wrong'
                }, code=HTTP_500_INTERNAL_SERVER_ERROR)
    
    @extend_schema(request=PostWCSerializer)
    @atomic
    def post(self,request):
        try:
            _request = PostWCSerializer(data={**request.data})
            if not _request.is_valid():
                return Response({
                    'message':"Invalid Request",
                    'errors':_request.errors
                },status=HTTP_422_UNPROCESSABLE_ENTITY)
            
            _model_serializer = WCModelSerializer(data={**request.data,'created_by':request.user.id})
            
            if _model_serializer.is_valid(raise_exception=True):
                _model_serializer.save()
                _trail = AuditTrailsSerializer(data={
                    'audit_type':'WC',
                    'tx_id':_model_serializer.data['id'],
                    'data':_model_serializer.data,
                    'created_by':request.user.id
                })
                if _trail.is_valid(raise_exception=True):
                    _trail.save()
                return Response({
                    'message':"Successfully saved data",
                    'data':_model_serializer.data
                },status=HTTP_201_CREATED)
            
            
        except Exception as ex:
            print(f'Failed to execute the API')
            print(format_exc(ex))
            raise APIException(detail={
                    'message':'Something went wrong'
                }, code=HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(request=PatchWCSerializer)
    @atomic
    def patch(self,request):
        try:
            _request = PatchWCSerializer(data={**request.data})
            if not _request.is_valid():
                return Response({
                    'message':"Invalid Request",
                    'errors':_request.errors
                },status=HTTP_422_UNPROCESSABLE_ENTITY)
            
            _id = _request.data['id']
            
            _dbp_model = WCMaster.objects.filter(id=_id).last()
            
            if _dbp_model is None:
                return Response(status=HTTP_404_NOT_FOUND,data={
                    'message':f"Cannot fetch data with id={_id}"
                })
            
            
            
            _model_serializer = WCModelSerializer(_dbp_model,data={**_request.data,'created_by':request.user.id})
            
            if _model_serializer.is_valid(raise_exception=True):
                _model_serializer.save()
                _trail = AuditTrailsSerializer(data={
                    'audit_type':'WC',
                    'tx_id':_model_serializer.data['id'],
                    'data':_model_serializer.data,
                    'created_by':request.user.id
                })
                if _trail.is_valid(raise_exception=True):
                    _trail.save()
                return Response({
                    'message':"Successfully saved data",
                    'data':_model_serializer.data
                },status=HTTP_201_CREATED)
            
            
        except Exception as ex:
            print(f'Failed to execute the API')
            print(format_exc(ex))
            raise APIException(detail={
                    'message':'Something went wrong'
                }, code=HTTP_500_INTERNAL_SERVER_ERROR)



@extend_schema(tags=["Calculation"])
class CalculationView(APIView):
    @extend_schema(request=CalculationsRequestSerializer)
    def post(self,request):
        try:
            _request = CalculationsRequestSerializer(data={**request.data})
            if not _request.is_valid():
                return Response({
                    'message':"Invalid Request",
                    'errors':_request.errors
                },status=HTTP_422_UNPROCESSABLE_ENTITY)
            
            
            _date =  datetime.strptime(_request.data['date_of_travel'],'%Y-%m-%d')
            
            weekday_map = {
                0:'Monday',
                1:'Tuesday',
                2:'Wednesday',
                3:'Thursday',
                4:'Friday',
                5:'Saturday',
                6:'Sunday'
            }
            # TODO: Not recommended use __contains instead
            _dbp_data = list(DBPMaster.objects.all().values())
            dbp_data = None
            for i in _dbp_data:
                if weekday_map[_date.weekday()] in i['applicable_days']:
                    dbp_data = i
            
            if dbp_data is None:
                raise ValueError("The base data is unavailaile.")
            
            
            # Calculate base price 
            print(dbp_data)
            _total_price = dbp_data.get('base_price',0)
            _total_dist_travelled = _request.data['distance_travelled']
            _waiting_time = _request.data['waiting_time']
            
            if _total_dist_travelled != 0:
                _dap_ceil_value = DAPMaster.objects.filter(distance_clip__gte=_request.data['amount_of_time_travelled']).order_by('-distance_clip').first()
                
                if _dap_ceil_value is None:
                    _dap_ceil_value = DAPMaster.objects.order_by('-distance_clip').first()
                
                # calculate additional price
                if _dap_ceil_value is not None:
                    _total_price += _dap_ceil_value.additional_price * _total_dist_travelled
                    _total_dist_travelled = 0
                    
                  
                
            _tmf_ceil_value = TMFMaster.objects.filter(time_clip__gte=_request.data['amount_of_time_travelled']).order_by('-time_clip').first()
            
            
            if _tmf_ceil_value is None:
                _tmf_ceil_value = TMFMaster.objects.order_by('-time_clip').first()
                
                if _tmf_ceil_value is not None:
                    _total_dist_travelled *= _tmf_ceil_value.multiplier


            _wc_ceil_value = WCMaster.objects.filter(time_clip__gte=_request.data['waiting_time']).order_by('-time_clip').first()
            
            if _wc_ceil_value is None:
                _wc_ceil_value = WCMaster.objects.order_by('-time_clip').first()
                
                if _wc_ceil_value is not None:
                    _waiting_charge = _waiting_time * _wc_ceil_value.charge_per_minute
                    _total_dist_travelled += _waiting_charge
            
            
            
            return Response({
                    'message':"Invalid Request",
                    'data':_total_price
                },status=HTTP_200_OK)
            
            
        
        except Exception as ex:
            print(f'Failed to execute the API')
            print(format_exc(ex))
            raise APIException(detail={
                    'message':'Something went wrong'
                }, code=HTTP_500_INTERNAL_SERVER_ERROR)

            