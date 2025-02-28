from django.contrib.auth.models import BaseUserManager

class CustomerManager(BaseUserManager):

    def create_user(self, email, username, bio=None, password=None, is_active=False):
        if email is None:
            raise ValueError('Email is required')
        
        if username is None:
            raise ValueError('Email is required')
        
        user = self.model(
            email = self.normalize_email(email),
            username=username,
            bio=bio
        )

        user.set_password(password)

        user.save(using=self.db)

        return user
    
    def create_superuser(self, email, username, password, bio=None):

        user = self.create_user(
            email = self.normalize_email(email),
            username=username,
            password=password,
            bio=bio
        )

        user.is_active=True
        user.is_admin=True
        user.is_staff=True
        user.is_superuser=True

        user.save(using=self.db)

        return user