from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    department = models.CharField(max_length=100, blank=True)
    office_name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {'Admin' if self.is_admin else 'User'}"
    
    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}".strip()

    @classmethod
    def create_with_user(cls, username, password, email=None, first_name='', last_name='', is_admin=False, **profile_fields):
        """Create user and profile in one go"""
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        if is_admin:
            user.is_staff = True
            user.save()
        
        profile = cls.objects.create(
            user=user,
            is_admin=is_admin,
            **profile_fields
        )
        return profile


class Ticket(models.Model):
    class Status(models.TextChoices):
        NEW = 'new', 'New'
        OPEN = 'open', 'Open'
        IN_PROGRESS = 'in_progress', 'In Progress'
        RESOLVED = 'resolved', 'Resolved'
        UNRESOLVED = 'unresolved', 'Unresolved'
        ARCHIVED = 'archived', 'Archived'
    
    class Priority(models.TextChoices):
        LOW = 'low', 'Low'
        MEDIUM = 'medium', 'Medium'
        HIGH = 'high', 'High'
        URGENT = 'urgent', 'Urgent'
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='tickets'
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='tickets'
    )
    assigned_to = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='assigned_tickets'
    )
    status = models.CharField(
        max_length=20, 
        choices=Status.choices, 
        default=Status.NEW
    )
    priority = models.CharField(
        max_length=20, 
        choices=Priority.choices, 
        default=Priority.MEDIUM
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    is_archived = models.BooleanField(default=False)
    spending = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,
        help_text="Cost associated with resolving this ticket"
    )
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['priority']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"#{self.id} - {self.title} ({self.get_status_display()})"
    
    def save(self, *args, **kwargs):
        # Set resolved_at when status becomes resolved
        if self.status == self.Status.RESOLVED and not self.resolved_at:
            self.resolved_at = timezone.now()
        
        # Set is_archived when status is archived
        if self.status == self.Status.ARCHIVED:
            self.is_archived = True
        
        super().save(*args, **kwargs)
    
    @property
    def age(self):
        """Return the age of the ticket in days"""
        return (timezone.now() - self.created_at).days
    
    @property
    def resolution_time(self):
        """Return the resolution time in days if resolved"""
        if self.resolved_at:
            return (self.resolved_at - self.created_at).days
        return None


class TicketMessage(models.Model):
    ticket = models.ForeignKey(
        Ticket, 
        on_delete=models.CASCADE, 
        related_name='messages'
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='ticket_messages'
    )
    message = models.TextField()
    is_internal = models.BooleanField(
        default=False,
        help_text="Check if this message should only be visible to staff"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
        verbose_name = "Ticket Message"
        verbose_name_plural = "Ticket Messages"
    
    def __str__(self):
        return f"Message #{self.id} on Ticket #{self.ticket.id}"


class Budget(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        help_text="Total allocated budget amount"
    )
    spent = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0,
        help_text="Amount already spent from this budget"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='budgets'
    )
    fiscal_year = models.PositiveSmallIntegerField(
        default=timezone.now().year,
        help_text="The fiscal year this budget applies to"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-fiscal_year', 'category']
        unique_together = ['category', 'fiscal_year']
    
    def __str__(self):
        return f"{self.name} (FY{self.fiscal_year}) - {self.category}"
    
    @property
    def remaining(self):
        return self.amount - self.spent
    
    @property
    def percentage_used(self):
        if self.amount <= 0:
            return 0
        return (self.spent / self.amount) * 100
    
    def update_spending(self, amount):
        """Update the spent amount and save"""
        self.spent += amount
        self.save()
        return self.spent