from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Count, Avg, Q, Sum
from django.utils import timezone
from datetime import datetime, timedelta, date
import json
import calendar
import csv
from django.template.loader import render_to_string
from weasyprint import HTML

from .models import Ticket, Category, UserProfile, Budget, TicketMessage
from .forms import BudgetForm


def check_admin_permission(user):
    """Check if user has admin permissions"""
    try:
        return user.userprofile.is_admin
    except UserProfile.DoesNotExist:
        return False


@login_required
def analytics_dashboard(request):
    """Comprehensive analytics dashboard"""
    if not check_admin_permission(request.user):
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('user_dashboard')
    
    # Only non-archived tickets for analytics
    tickets = Ticket.objects.filter(is_archived=False)
    
    # Time periods
    today = timezone.now().date()
    last_30_days = today - timedelta(days=30)
    last_90_days = today - timedelta(days=90)
    last_year = today - timedelta(days=365)
    
    # Basic statistics (using filtered tickets)
    total_tickets = tickets.count()
    tickets_last_30 = tickets.filter(created_at__date__gte=last_30_days).count()
    tickets_last_90 = tickets.filter(created_at__date__gte=last_90_days).count()
    
    # Category statistics (using filtered tickets)
    category_stats = Category.objects.annotate(
        ticket_count=Count('tickets', filter=Q(tickets__is_archived=False)),
        new_tickets=Count('tickets', filter=Q(tickets__status='new', tickets__is_archived=False)),
        open_tickets=Count('tickets', filter=Q(tickets__status='open', tickets__is_archived=False)),
        in_progress_tickets=Count('tickets', filter=Q(tickets__status='in_progress', tickets__is_archived=False)),
        resolved_tickets=Count('tickets', filter=Q(tickets__status='resolved', tickets__is_archived=False)),
        unresolved_tickets=Count('tickets', filter=Q(tickets__status='unresolved', tickets__is_archived=False))
    ).order_by('-ticket_count')
    
    # Priority statistics (using filtered tickets)
    priority_stats = []
    for priority in ['low', 'medium', 'high', 'urgent']:
        stats = {
            'priority': priority,
            'total': tickets.filter(priority=priority).count(),
            'new': tickets.filter(priority=priority, status='new').count(),
            'open': tickets.filter(priority=priority, status='open').count(),
            'in_progress': tickets.filter(priority=priority, status='in_progress').count(),
            'resolved': tickets.filter(priority=priority, status='resolved').count(),
            'unresolved': tickets.filter(priority=priority, status='unresolved').count()
        }
        priority_stats.append(stats)
    
    # Monthly trends (using filtered tickets)
    monthly_trends = []
    for i in range(12):
        date = today.replace(day=1) - timedelta(days=30*i)
        month_tickets = tickets.filter(
            created_at__year=date.year,
            created_at__month=date.month
        ).count()
        monthly_trends.append({
            'month': date.strftime('%B %Y'),
            'tickets': month_tickets
        })
    
    # Top users (using filtered tickets)
    top_users = tickets.values('user__username').annotate(
        ticket_count=Count('id')
    ).order_by('-ticket_count')[:5]
    
    # Response times by category (using filtered tickets)
    response_times = []
    for category in Category.objects.all():
        cat_tickets = tickets.filter(category=category)
        if cat_tickets.exists():
            total_seconds = sum(
                (ticket.created_at - ticket.updated_at).total_seconds()
                for ticket in cat_tickets
            )
            avg_seconds = total_seconds / cat_tickets.count()
            avg_hours = avg_seconds / 3600
            
            response_times.append({
                'category': category.name,
                'avg_hours': round(avg_hours, 2)
            })
    
    context = {
        'total_tickets': total_tickets,
        'tickets_last_30': tickets_last_30,
        'tickets_last_90': tickets_last_90,
        'category_stats': category_stats,
        'priority_stats': json.dumps(priority_stats),
        'monthly_trends': json.dumps(monthly_trends),
        'top_users': top_users,
        'response_times': json.dumps(response_times)
    }
    
    return render(request, 'tickets/analytics_dashboard.html', context)


@login_required
def forecasting_dashboard(request):
    """Forecasting and predictive analytics"""
    if not check_admin_permission(request.user):
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('user_dashboard')
    
    # Get all tickets for forecasting (including archived)
    all_tickets = Ticket.objects.all()
    
    # Historical data for forecasting (all tickets)
    today = timezone.now().date()
    
    # Get last 12 months of data (all tickets)
    historical_data = []
    for i in range(12):
        date_obj = today.replace(day=1) - timedelta(days=30*i)
        month_tickets = all_tickets.filter(
            created_at__year=date_obj.year,
            created_at__month=date_obj.month
        ).count()
        historical_data.append({
            'month': date_obj.strftime('%Y-%m'),
            'tickets': month_tickets
        })
    
    # Calculate forecast (using all tickets)
    def calculate_forecast(data):
        if len(data) < 2:
            return []
        
        # Calculate trend
        x_values = list(range(len(data)))
        y_values = [item['tickets'] for item in data]
        
        n = len(data)
        sum_x = sum(x_values)
        sum_y = sum(y_values)
        sum_xy = sum(x * y for x, y in zip(x_values, y_values))
        sum_x2 = sum(x * x for x in x_values)
        
        # Linear regression: y = mx + b
        m = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
        b = (sum_y - m * sum_x) / n
        
        # Generate forecast for next 6 months
        forecast = []
        for i in range(6):
            x = len(data) + i  # Future month
            predicted_tickets = int(m * x + b)
            forecast.append({
                'month': len(data) + i + 1,  # Month number
                'predicted_tickets': max(0, predicted_tickets)  # Ensure non-negative
            })
        
        return forecast
    
    forecast_data = calculate_forecast(historical_data)
    
    # Category forecasts (all tickets)
    category_forecasts = []
    for category in Category.objects.all():
        cat_tickets = all_tickets.filter(category=category)
        cat_historical = []
        for i in range(12):
            date_obj = today.replace(day=1) - timedelta(days=30*i)
            month_tickets = cat_tickets.filter(
                created_at__year=date_obj.year,
                created_at__month=date_obj.month
            ).count()
            cat_historical.append({
                'month': date_obj.strftime('%Y-%m'),
                'tickets': month_tickets
            })
        
        forecast = calculate_forecast(cat_historical)
        category_forecasts.append({
            'category': category.name,
            'forecast': forecast
        })
    
    # Status-based forecasts (all tickets)
    status_forecasts = []
    for status in Ticket.Status.values:
        status_tickets = all_tickets.filter(status=status)
        status_historical = []
        for i in range(12):
            date_obj = today.replace(day=1) - timedelta(days=30*i)
            month_tickets = status_tickets.filter(
                created_at__year=date_obj.year,
                created_at__month=date_obj.month
            ).count()
            status_historical.append({
                'month': date_obj.strftime('%Y-%m'),
                'tickets': month_tickets
            })
        
        forecast = calculate_forecast(status_historical)
        status_forecasts.append({
            'status': status,
            'forecast': forecast
        })
    
    # Predicted workload (using filtered tickets)
    predicted_workload = []
    for i in range(6):
        future_date = today.replace(day=1) + timedelta(days=30*(i+1))
        predicted_workload.append({
            'month': future_date.strftime('%B %Y'),
            'tickets': forecast_data[i]['predicted_tickets'] if i < len(forecast_data) else 0
        })
    
    # Resource recommendations based on forecast
    resource_recommendations = []
    current_open = all_tickets.filter(status__in=['open', 'in_progress']).count()
    for month in predicted_workload:
        predicted_tickets = month['tickets']
        if predicted_tickets > current_open * 1.2:
            resource_recommendations.append({
                'month': month['month'],
                'tickets': predicted_tickets,
                'recommendation': 'Consider adding staff'
            })
        elif predicted_tickets < current_open * 0.8:
            resource_recommendations.append({
                'month': month['month'],
                'tickets': predicted_tickets,
                'recommendation': 'Consider reducing staff'
            })
    
    # Seasonal patterns (using filtered tickets)
    seasonal_data = []
    for month in range(1, 13):
        month_tickets = all_tickets.filter(
            created_at__month=month
        ).count()
        distinct_years = all_tickets.filter(
            created_at__month=month
        ).values('created_at__year').distinct().count()
        
        # Avoid division by zero
        if distinct_years > 0:
            monthly_avg = month_tickets / distinct_years
        else:
            monthly_avg = 0
            
        seasonal_data.append({
            'month': calendar.month_name[month],
            'avg_tickets': round(monthly_avg, 1)
        })
    
    context = {
        'historical_data': json.dumps(historical_data),
        'forecast_data': json.dumps(forecast_data),
        'category_forecasts': category_forecasts,
        'predicted_workload': predicted_workload,
        'resource_recommendations': resource_recommendations,
        'seasonal_data': json.dumps(seasonal_data),
        'current_open_tickets': current_open
    }
    
    return render(request, 'tickets/forecasting_dashboard.html', context)


@login_required
def budget_management(request):
    """Budget management and tracking"""
    if not check_admin_permission(request.user):
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('user_dashboard')
    
    budgets = Budget.objects.select_related('category').all()
    
    # Calculate totals
    total_allocated = budgets.aggregate(Sum('amount'))['amount__sum'] or 0
    total_spent = budgets.aggregate(Sum('spent'))['spent__sum'] or 0
    total_remaining = total_allocated - total_spent
    
    # Budget utilization by category
    budget_utilization = []
    for budget in budgets:
        utilization_percent = (budget.spent / budget.amount * 100) if budget.amount > 0 else 0
        status = 'success'
        if utilization_percent > 90:
            status = 'danger'
        elif utilization_percent > 75:
            status = 'warning'
        elif utilization_percent > 50:
            status = 'info'
        
        budget_utilization.append({
            'budget': budget,
            'utilization_percent': round(utilization_percent, 1),
            'status': status
        })
    
    # Monthly spending trends
    monthly_spending = []
    today = timezone.now().date()
    for i in range(6):
        date_obj = today.replace(day=1) - timedelta(days=30*i)
        # Mock spending data - in real implementation, this would come from actual expense tracking
        month_spending = total_spent / 6  # Simplified for demo
        monthly_spending.append({
            'month': date_obj.strftime('%B %Y'),
            'spending': float(month_spending)  # Convert Decimal to float
        })
    monthly_spending.reverse()
    
    # Convert monthly_spending to float values before JSON serialization
    monthly_spending = [{
        'month': item['month'],
        'spending': float(item['spending'])  # Ensure spending is float
    } for item in monthly_spending]
    
    # Cost per ticket analysis
    total_tickets = Ticket.objects.count()
    cost_per_ticket = (total_spent / total_tickets) if total_tickets > 0 else 0
    
    # Category cost analysis
    category_costs = []
    # Get all tickets with assigned categories
    categorized_tickets = Ticket.objects.filter(category__isnull=False)
    
    for category in Category.objects.all():
        cat_budget = budgets.filter(category=category).first()
        if not cat_budget:
            continue
            
        # Count tickets assigned to this category
        cat_tickets = categorized_tickets.filter(category=category).count()
        
        if cat_tickets > 0:
            cost_per_cat_ticket = cat_budget.spent / cat_tickets
            category_costs.append({
                'category': category.name,
                'total_spent': cat_budget.spent,
                'tickets': cat_tickets,
                'cost_per_ticket': round(cost_per_cat_ticket, 2)
            })
    
    # Budget alerts
    alerts = []
    for budget in budgets:
        utilization = (budget.spent / budget.amount * 100) if budget.amount > 0 else 0
        if utilization > 90:
            alerts.append({
                'type': 'danger',
                'message': f'{budget.category.name} budget is {utilization:.1f}% utilized',
                'budget': budget
            })
        elif utilization > 75:
            alerts.append({
                'type': 'warning',
                'message': f'{budget.category.name} budget is {utilization:.1f}% utilized',
                'budget': budget
            })
    
    context = {
        'budgets': budgets,
        'budget_utilization': budget_utilization,
        'total_allocated': total_allocated,
        'total_spent': total_spent,
        'total_remaining': total_remaining,
        'monthly_spending': json.dumps(monthly_spending),
        'cost_per_ticket': round(cost_per_ticket, 2),
        'category_costs': category_costs,
        'alerts': alerts,
    }
    
    return render(request, 'tickets/budget_management.html', context)


@login_required
def create_budget(request):
    """Create new budget"""
    if not check_admin_permission(request.user):
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('user_dashboard')
    
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Budget created successfully!')
            return redirect('budget_management')
    else:
        form = BudgetForm()
    
    return render(request, 'tickets/create_budget.html', {'form': form})


@login_required
def edit_budget(request, budget_id):
    """Edit existing budget"""
    if not check_admin_permission(request.user):
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('user_dashboard')
    
    budget = Budget.objects.get(id=budget_id)
    
    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            messages.success(request, 'Budget updated successfully!')
            return redirect('budget_management')
    else:
        form = BudgetForm(instance=budget)
    
    return render(request, 'tickets/edit_budget.html', {'form': form, 'budget': budget})


@login_required
def download_budget_report(request):
    """Download budget report as CSV with professional formatting"""
    if not check_admin_permission(request.user):
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('user_dashboard')
    
    # Create HTTP response with CSV content type
    timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="Budget_Report_{timestamp}.csv"'
    
    writer = csv.writer(response)
    
    # Write report header with metadata
    writer.writerow(['BUDGET MANAGEMENT REPORT'])
    writer.writerow(['Generated on:', timezone.now().strftime('%B %d, %Y at %I:%M %p')])
    writer.writerow(['Report Type:', 'Complete Budget Analysis'])
    writer.writerow([])  # Empty row for spacing
    
    # Get all budgets with related data
    budgets = Budget.objects.select_related('category').all().order_by('fiscal_year', 'category__name')
    
    # Calculate summary statistics
    total_allocated = budgets.aggregate(Sum('amount'))['amount__sum'] or 0
    total_spent = budgets.aggregate(Sum('spent'))['spent__sum'] or 0
    total_remaining = total_allocated - total_spent
    overall_utilization = (total_spent / total_allocated * 100) if total_allocated > 0 else 0
    
    # Write summary section
    writer.writerow(['EXECUTIVE SUMMARY'])
    writer.writerow(['Total Budgets:', len(budgets)])
    writer.writerow(['Total Allocated:', f'${total_allocated:,.2f}'])
    writer.writerow(['Total Spent:', f'${total_spent:,.2f}'])
    writer.writerow(['Total Remaining:', f'${total_remaining:,.2f}'])
    writer.writerow(['Overall Utilization:', f'{overall_utilization:.1f}%'])
    writer.writerow([])  # Empty row for spacing
    
    # Write detailed budget data headers
    writer.writerow(['DETAILED BUDGET BREAKDOWN'])
    writer.writerow([
        'Budget Name',
        'Category',
        'Fiscal Year',
        'Allocated Amount',
        'Amount Spent',
        'Remaining Balance',
        'Utilization Rate',
        'Budget Status',
        'Created Date',
        'Last Updated',
        'Days Active'
    ])
    
    # Write budget data rows
    for budget in budgets:
        # Use the spent amount from the budget model
        remaining = budget.remaining
        utilization = budget.percentage_used
        
        # Determine status based on utilization
        if utilization >= 90:
            status = '🔴 CRITICAL'
        elif utilization >= 75:
            status = '🟡 WARNING'
        elif utilization >= 50:
            status = '🟠 CAUTION'
        else:
            status = '🟢 GOOD'
        
        # Calculate days active
        days_active = (timezone.now().date() - budget.created_at.date()).days
        
        # Write budget data row with better formatting
        writer.writerow([
            budget.name,
            budget.category.name,
            f'FY {budget.fiscal_year}',
            f'${budget.amount:,.2f}',
            f'${budget.spent:,.2f}',
            f'${remaining:,.2f}',
            f'{utilization:.1f}%',
            status,
            budget.created_at.strftime('%m/%d/%Y'),
            budget.updated_at.strftime('%m/%d/%Y'),
            f'{days_active} days'
        ])
    
    # Add footer with additional information
    writer.writerow([])  # Empty row for spacing
    writer.writerow(['BUDGET STATUS LEGEND'])
    writer.writerow(['🟢 GOOD:', 'Less than 50% utilized'])
    writer.writerow(['🟠 CAUTION:', '50-74% utilized'])
    writer.writerow(['🟡 WARNING:', '75-89% utilized'])
    writer.writerow(['🔴 CRITICAL:', '90% or more utilized'])
    writer.writerow([])  # Empty row for spacing
    writer.writerow(['Report generated by SUPERDOLL IT Help Desk System'])
    writer.writerow(['For questions, contact your system administrator'])
    
    return response


@login_required
def budget_report_table(request):
    """Display budget report in HTML table format"""
    if not check_admin_permission(request.user):
        messages.error(request, 'Access denied. Admin privileges required.')
        return redirect('user_dashboard')
    
    # Get all budgets with related data
    budgets = Budget.objects.select_related('category').all().order_by('fiscal_year', 'category__name')
    
    # Calculate summary statistics
    total_allocated = budgets.aggregate(Sum('amount'))['amount__sum'] or 0
    total_spent = budgets.aggregate(Sum('spent'))['spent__sum'] or 0
    total_remaining = total_allocated - total_spent
    overall_utilization = (total_spent / total_allocated * 100) if total_allocated > 0 else 0
    
    # Prepare budget data with enhanced information
    budget_data = []
    for budget in budgets:
        remaining = budget.remaining
        utilization = budget.percentage_used
        
        # Determine status based on utilization
        if utilization >= 90:
            status = 'CRITICAL'
            status_class = 'danger'
        elif utilization >= 75:
            status = 'WARNING'
            status_class = 'warning'
        elif utilization >= 50:
            status = 'CAUTION'
            status_class = 'info'
        else:
            status = 'GOOD'
            status_class = 'success'
        
        # Calculate days active
        days_active = (timezone.now().date() - budget.created_at.date()).days
        
        budget_data.append({
            'budget': budget,
            'remaining': remaining,
            'utilization': utilization,
            'status': status,
            'status_class': status_class,
            'days_active': days_active
        })
    
    context = {
        'budgets': budget_data,
        'total_allocated': total_allocated,
        'total_spent': total_spent,
        'total_remaining': total_remaining,
        'overall_utilization': overall_utilization,
        'report_date': timezone.now(),
        'total_budgets': len(budgets)
    }
    
    return render(request, 'tickets/budget_report_table.html', context)


@login_required
def api_analytics_data(request):
    """API endpoint for analytics data"""
    if not check_admin_permission(request.user):
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    data_type = request.GET.get('type', 'overview')
    
    # Only non-archived tickets for API
    tickets = Ticket.objects.filter(is_archived=False)
    
    if data_type == 'overview':
        # Real-time overview data (using filtered tickets)
        data = {
            'total_tickets': tickets.count(),
            'open_tickets': tickets.filter(status='open').count(),
            'in_progress': tickets.filter(status='in_progress').count(),
            'resolved_today': tickets.filter(
                status='resolved',
                updated_at__date=timezone.now().date()
            ).count(),
            'avg_response_time': round(
                tickets.aggregate(avg_time=Avg(
                    ExpressionWrapper(
                        F('updated_at') - F('created_at'),
                        output_field=DurationField()
                    )
                ))['avg_time'].total_seconds() / 3600,
                2
            )
        }
    
    elif data_type == 'categories':
        categories = []
        for category in Category.objects.all():
            cat_tickets = tickets.filter(category=category)
            if cat_tickets.exists():
                total_seconds = sum(
                    (ticket.updated_at - ticket.created_at).total_seconds()
                    for ticket in cat_tickets
                )
                avg_seconds = total_seconds / cat_tickets.count()
                avg_hours = avg_seconds / 3600
                
                categories.append({
                    'name': category.name,
                    'avg_resolution_hours': round(avg_hours, 2)
                })
        
        data = {
            'categories': categories,
            'overall_satisfaction': 4.2  # Mock data
        }
    
    else:
        data = {'error': 'Invalid data type'}
    
    return JsonResponse(data)
