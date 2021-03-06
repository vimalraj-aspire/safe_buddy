from django.shortcuts import render
from .serializers import SBUserSerializer, PasswordResetSerializer, FriendSertializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from serializers import UserSerializer
from models import UserProfile, Friend
from rest_framework.request import Request
from safe_buddy import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.db.models import Q
from rest_framework import viewsets
from models import EmployeeRole, Department, EmergencyContact
from serializers import DepartmentSerializer

@api_view(['GET'])
@permission_classes((AllowAny, ))
def get_user(request, username):
  ''' Function to user detail '''
  user = UserProfile.objects.filter(Q(user__username=username) | Q(aceid__istartswith=username))
  if user:
    serializer = SBUserSerializer(user, many=True)
    return Response(serializer.data)
  else:  
    return Response({'status': 'failed', 'msg': settings.API_ERRORS.get('USER_DOES_NOT_EXISTS')}, status=status.HTTP_404_NOT_FOUND)



class SBUserList(APIView):
    """
    List all SB users, or create a new SB user.
    """
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        user = UserProfile.objects.all().exclude(user__is_superuser=1)
        serializer = SBUserSerializer(user, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer_context = {
        'request': Request(request),
        }

        user_data = {}
        user_data['email'] = request.data.pop('email')[0]
        user_data['username'] = request.data.pop('username')[0]
        user_data['password'] = request.data.pop('password')[0]
        user_data['first_name'] = request.data.pop('first_name')[0]

        user_seriliazer = UserSerializer(data=user_data)
        if user_seriliazer.is_valid(request.data):
            user  = user_seriliazer.save()
            request.data['user'] = user.id            
            serializer = SBUserSerializer(data=request.data, context=serializer_context)
            if serializer.is_valid():
                employee = serializer.save()
                if request.data.get('user_type') == 'EMPLOYEE':
                    EmployeeRole.objects.create(employee=employee, department= Department.objects.get(pk=request.data.get('department')), role=request.data.get('role'))
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
              user.delete()
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(GenericAPIView):
    serializer_class = PasswordResetSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.POST.get('email',''))
        if serializer.is_valid():
            serializer.save()
            return Response({'success':True})
        else:
            return Response(
                {"failed": serializer.errors},
                status=400
            )

@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, ))
def add_trackee(request, username):
  ''' Function to add add trackee'''
  try:    
    userprofile = UserProfile.objects.get(user=request.user)
    trackee = UserProfile.objects.get(user__username=username)
    friend = Friend.objects.filter(user_profile=userprofile, friend_profile=trackee)
    if friend:
        return Response({'status': 'failed', 'msg': 'Already the user is in trackee list'}, status=status.HTTP_404_NOT_FOUND)
    else:
         Friend.objects.create(user_profile=userprofile, friend_profile=trackee)
         return Response({'status': 'success', 'msg': 'User has been added in trackee list'}, status=status.HTTP_404_NOT_FOUND)
  except UserProfile.DoesNotExist:
    return Response({'status': 'failed', 'msg': settings.API_ERRORS.get('USER_DOES_NOT_EXISTS')}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def my_trackees(request):
    userprofile = UserProfile.objects.get(user=request.user)
    trackees = Friend.objects.filter(user_profile=userprofile)
    if trackees:
      serializer = FriendSertializer(trackees, many=True)
      return Response(serializer.data)
    else:
      return Response({'status': 'failed', 'msg': 'No trackee found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def who_are_all_tracking_me(request):
    userprofile = UserProfile.objects.get(user=request.user)
    trackers = Friend.objects.filter(friend_profile=userprofile)
    if trackers:
      serializer = FriendSertializer(trackers, many=True)
      return Response(serializer.data)
    else:
      return Response({'status': 'failed', 'msg': 'No trackers found'}, status=status.HTTP_404_NOT_FOUND)


class DepartmentViewSet(viewsets.ModelViewSet):
  def get_objects():
    '''
    Function to return data from cache if exists
    '''
  serializer_class = DepartmentSerializer
  queryset =  Department.objects.all()


class DepartmentDetailView(APIView):
  """
  Retrieve, update or delete a department instance.
  """
  def get_object(self, id):
    try:
        return Department.objects.get(id=id)
    except Department.DoesNotExist:
        raise Http404

  def get(self, request, id, format=None):
    department = self.get_object(id)
    serializer = DepartmentSerializer(department)
    return Response(serializer.data)

  def put(self, request, id, format=None):
    department = self.get_object(id)
    serializer = DepartmentSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def delete(self, request, id, format=None):
    department = self.get_object(id)
    department.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['POST'])
def map_employee(request, username):
  ''' Function to employee to a department'''
  employee = UserProfile.objects.get(user__username=username)
  # if int(request.data.get('role')) == settings.ROLES.get('MANAGER') and EmployeeRole.objects.filter(department= Department.objects.get(pk=request.data.get('department')), role=settings.ROLES.get('MANAGER')):
  #     return Response({'status': 'failed', 'msg': settings.API_ERRORS.get('TEAM_ALREADY_HAVE_A_MANAGER')}, status=status.HTTP_412_PRECONDITION_FAILED)

  EmployeeRole.objects.create(employee=employee, department=Department.objects.get(pk=request.data.get('department')), role=2)

  return Response({'status':'success', 'msg':'User mapped to a department'},status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_employees_by_department(request, department_id):
  ''' Function to get location '''  
  friends = EmployeeRole.objects.filter(department=department_id).values('employee')
  friends_location = []
  for friend in friends:
    profile = UserProfile.objects.get(id=friend.get('employee'))    
    friends_location.append({'aceid':profile.aceid, 'first_name': profile.user.first_name, 'username': profile.user.username, 'user_relation': profile.user_relation, 'user_type': profile.user_type})
  return Response(friends_location)




@api_view(['POST'])
def create_contact(request):
  ''' Function to employee to a department'''
  employee = UserProfile.objects.get(user=request.user)

  EmergencyContact.objects.create(employee=employee,name=request.data.get('name'), number = request.data.get('number'))

  return Response({'status':'success', 'msg':'Emergencey contact has been created'},status=status.HTTP_201_CREATED)

@api_view(['GET'])
def list_contacts(request):
  ''' Function to employee to a department'''
  employee = UserProfile.objects.get(user=request.user)
  e_contacts = []
  for contact in EmergencyContact.objects.filter(employee=employee):
    e_contacts.append({'name':contact.name, 'number': contact.number})

  return Response(e_contacts)

