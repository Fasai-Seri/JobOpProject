from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from user_profiles.models import User, Professor, Student, Employer

class CustomAuthentication(ModelBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(username=username)
            
            if user.check_password(password):
                CustomAuthentication.if_first_time_set_up()

                user.groups.clear()
                if Professor.objects.filter(user=user).exists():
                    if not user.groups.filter(name="Professor").exists():
                        user.groups.add(Group.objects.get(name="Professor"))
                if Student.objects.filter(user=user).exists():
                    if not user.groups.filter(name="Student").exists():
                        user.groups.add(Group.objects.get(name="Student"))
                if Employer.objects.filter(user=user).exists():
                    if not user.groups.filter(name="Employer").exists():
                        user.groups.add(Group.objects.get(name="Employer"))
                return user
            return None
        except User.DoesNotExist:
            return None



    @staticmethod
    def if_first_time_set_up():
        if not Group.objects.filter(name="Professor").exists():
            Group.objects.create(name="Professor")
        if not Group.objects.filter(name="Student").exists():
            Group.objects.create(name="Student")
        if not Group.objects.filter(name="Employer").exists():
            Group.objects.create(name="Employer")
        

        if not Permission.objects.filter(codename="is_professor").exists():
            Permission.objects.create(
                codename="is_professor",
                name="User is Professor",
                content_type=ContentType.objects.get_for_model(User),
            )
        if not Permission.objects.filter(codename="is_student").exists():
            Permission.objects.create(
                codename="is_student",
                name="User is Student",
                content_type=ContentType.objects.get_for_model(User),
            )
        if not Permission.objects.filter(codename="is_employer").exists():
            Permission.objects.create(
                codename="is_employer",
                name="User is Employer",
                content_type=ContentType.objects.get_for_model(User),
            )

        if not Group.objects.get(name="Professor").permissions.filter(codename="is_professor").exists():
            Group.objects.get(name="Professor").permissions.add(Permission.objects.get(codename="is_professor"))
        if not Group.objects.get(name="Student").permissions.filter(codename="is_student").exists():
            Group.objects.get(name="Student").permissions.add(Permission.objects.get(codename="is_student"))
        if not Group.objects.get(name="Employer").permissions.filter(codename="is_employer").exists():
            Group.objects.get(name="Employer").permissions.add(Permission.objects.get(codename="is_employer"))