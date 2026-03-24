from django.contrib import admin
from .models import Doctor, Appointment, Review, UserProfile


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization', 'location', 'experience', 'average_rating', 'total_reviews')
    list_filter = ('specialization', 'location', 'experience')
    search_fields = ('name', 'specialization', 'clinic_name')
    readonly_fields = ('average_rating', 'total_reviews', 'created_at', 'updated_at')
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'email', 'contact', 'bio')
        }),
        ('Professional Details', {
            'fields': ('specialization', 'experience', 'qualification', 'clinic_name')
        }),
        ('Location', {
            'fields': ('location',)
        }),
        ('Ratings', {
            'fields': ('average_rating', 'total_reviews'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'date', 'time', 'status')
    list_filter = ('status', 'date', 'doctor')
    search_fields = ('patient__username', 'doctor__name')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Appointment Details', {
            'fields': ('patient', 'doctor', 'date', 'time')
        }),
        ('Status & Notes', {
            'fields': ('status', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'user', 'rating', 'title', 'created_at')
    list_filter = ('rating', 'doctor', 'created_at')
    search_fields = ('doctor__name', 'user__username', 'title', 'comment')
    readonly_fields = ('created_at', 'updated_at', 'helpful_count')
    fieldsets = (
        ('Review Details', {
            'fields': ('doctor', 'user', 'rating', 'title', 'comment')
        }),
        ('Engagement', {
            'fields': ('helpful_count',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'city', 'created_at')
    list_filter = ('city', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone', 'city')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Personal Information', {
            'fields': ('bio', 'phone', 'date_of_birth')
        }),
        ('Address', {
            'fields': ('address', 'city', 'state')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )