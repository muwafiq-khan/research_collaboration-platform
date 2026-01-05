from django.shortcuts import render, redirect, get_object_or_404
from django.db import models
from .models import User, Post, Project, Problem, Field, Subfield, CollaborationRequest

# ==============================================================================
# FEATURE 1: LOGIN SYSTEM
# ==============================================================================

def login_view(request):
    """Display login page with user dropdown"""
    # SQL: SELECT * FROM user WHERE id = <user_id>;
    # SQL: SELECT * FROM user ORDER BY name ASC;
    
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = get_object_or_404(User, id=user_id)
        
        # Store user info in session
        request.session['user_id'] = user.id
        request.session['user_name'] = user.name
        request.session['user_type'] = user.user_type
        
        return redirect('feed')
    
    # GET request - show login page
    # SQL: SELECT * FROM user ORDER BY name ASC;
    users = User.objects.all().order_by('name')
    return render(request, 'core/login.html', {'users': users})


def logout_view(request):
    """Logout user and clear session"""
    # No SQL - just clears session data
    request.session.flush()
    return redirect('login')


# ==============================================================================
# FEATURE 4: WORLD FEED
# ==============================================================================

def feed_view(request):
    """Display world feed with all posts"""
    # SQL: SELECT post.*, user.id, user.name, user.institution 
    #      FROM post 
    #      JOIN user ON post.author_id = user.id 
    #      ORDER BY post.created_at DESC;
    
    # SQL: SELECT COUNT(*) FROM collaboration_request 
    #      WHERE receiver_id = <current_user> AND status = 'pending';
    
    # Check if user is logged in
    if not request.session.get('user_id'):
        return redirect('login')
    
    # Get all posts
    posts = Post.objects.all().select_related('author')
    
    # Get pending collaboration requests count for current user
    user_id = request.session.get('user_id')
    pending_requests_count = CollaborationRequest.objects.filter(
        receiver_id=user_id,
        status='pending'
    ).count()
    
    context = {
        'posts': posts,
        'pending_requests_count': pending_requests_count,
    }
    return render(request, 'core/feed.html', context)


def create_post_view(request):
    """Create a new post"""
    # SQL: SELECT * FROM user WHERE id = <current_user_id>;
    # SQL: INSERT INTO post (author_id, content, created_at) 
    #      VALUES (<user_id>, <content>, NOW());
    
    if not request.session.get('user_id'):
        return redirect('login')
    
    if request.method == 'POST':
        content = request.POST.get('content')
        user_id = request.session.get('user_id')
        user = get_object_or_404(User, id=user_id)
        
        Post.objects.create(
            author=user,
            content=content
        )
    
    return redirect('feed')


def collaborate_post_view(request, post_id):
    """Send collaboration request for a post"""
    # SQL: SELECT * FROM post WHERE id = <post_id>;
    # SQL: SELECT * FROM user WHERE id = <current_user_id>;
    # SQL: SELECT * FROM collaboration_request 
    #      WHERE sender_id = <sender_id> AND receiver_id = <receiver_id> AND post_id = <post_id> 
    #      LIMIT 1;
    # SQL: INSERT INTO collaboration_request (sender_id, receiver_id, post_id, project_id, status, created_at)
    #      VALUES (<sender_id>, <receiver_id>, <post_id>, NULL, 'pending', NOW());
    
    if not request.session.get('user_id'):
        return redirect('login')
    
    post = get_object_or_404(Post, id=post_id)
    sender_id = request.session.get('user_id')
    sender = get_object_or_404(User, id=sender_id)
    
    # Don't send request to yourself
    if sender.id != post.author.id:
        # Check if request already exists
        existing = CollaborationRequest.objects.filter(
            sender=sender,
            receiver=post.author,
            post=post
        ).first()
        
        if not existing:
            CollaborationRequest.objects.create(
                sender=sender,
                receiver=post.author,
                post=post,
                status='pending'
            )
    
    return redirect('feed')


# ==============================================================================
# FEATURE 2: USER PROFILE & SEARCH RESEARCHERS
# ==============================================================================

def profile_view(request, user_id):
    """Display user profile with their projects"""
    # SQL: SELECT * FROM user WHERE id = <user_id>;
    # SQL: SELECT project.*, field.name AS field_name, subfield.name AS subfield_name
    #      FROM project
    #      JOIN field ON project.field_id = field.name
    #      JOIN subfield ON project.subfield_id = subfield.id
    #      WHERE project.owner_id = <user_id>
    #      ORDER BY project.created_at DESC;
    
    if not request.session.get('user_id'):
        return redirect('login')
    
    profile_user = get_object_or_404(User, id=user_id)
    projects = Project.objects.filter(owner=profile_user).select_related('field', 'subfield')
    
    context = {
        'profile_user': profile_user,
        'projects': projects,
    }
    return render(request, 'core/profile.html', context)


def search_researchers_view(request):
    """Search and filter researchers"""
    # SQL: SELECT name FROM field ORDER BY name;
    # SQL: SELECT * FROM user 
    #      WHERE user_type = 'researcher'
    #      AND field LIKE '%<field_filter>%'
    #      AND country LIKE '%<country_filter>%'
    #      AND institution LIKE '%<institution_filter>%'
    #      ORDER BY name;
    
    if not request.session.get('user_id'):
        return redirect('login')
    
    # Get all fields for dropdown
    fields = Field.objects.all()
    
    # Start with all researchers
    researchers = User.objects.filter(user_type='researcher')
    
    # Check if search was performed
    searched = False
    
    # Apply filters if provided
    field_filter = request.GET.get('field')
    country_filter = request.GET.get('country')
    institution_filter = request.GET.get('institution')
    
    if field_filter or country_filter or institution_filter:
        searched = True
        
        if field_filter:
            researchers = researchers.filter(field__icontains=field_filter)
        
        if country_filter:
            researchers = researchers.filter(country__icontains=country_filter)
        
        if institution_filter:
            researchers = researchers.filter(institution__icontains=institution_filter)
    
    context = {
        'fields': fields,
        'researchers': researchers,
        'searched': searched,
    }
    return render(request, 'core/search_researchers.html', context)


def collaborate_project_view(request, project_id):
    """Send collaboration request for a project"""
    # SQL: SELECT * FROM project WHERE id = <project_id>;
    # SQL: SELECT * FROM user WHERE id = <current_user_id>;
    # SQL: SELECT * FROM collaboration_request 
    #      WHERE sender_id = <sender_id> AND receiver_id = <receiver_id> AND project_id = <project_id>
    #      LIMIT 1;
    # SQL: INSERT INTO collaboration_request (sender_id, receiver_id, project_id, post_id, status, created_at)
    #      VALUES (<sender_id>, <receiver_id>, <project_id>, NULL, 'pending', NOW());
    
    if not request.session.get('user_id'):
        return redirect('login')
    
    project = get_object_or_404(Project, id=project_id)
    sender_id = request.session.get('user_id')
    sender = get_object_or_404(User, id=sender_id)
    
    # Don't send request to yourself
    if sender.id != project.owner.id:
        # Check if request already exists
        existing = CollaborationRequest.objects.filter(
            sender=sender,
            receiver=project.owner,
            project=project
        ).first()
        
        if not existing:
            CollaborationRequest.objects.create(
                sender=sender,
                receiver=project.owner,
                project=project,
                status='pending'
            )
    
    return redirect('profile', user_id=project.owner.id)


def project_detail_view(request, project_id):
    """Project details - placeholder for now"""
    # SQL: SELECT * FROM project WHERE id = <project_id>;
    
    if not request.session.get('user_id'):
        return redirect('login')
    
    project = get_object_or_404(Project, id=project_id)
    return redirect('profile', user_id=project.owner.id)


# ==============================================================================
# FEATURE 3: PROBLEM SEARCH
# ==============================================================================

def search_problems_view(request):
    """Search problems by field and subfield"""
    # SQL: SELECT name FROM field ORDER BY name;
    # SQL: SELECT subfield.id, subfield.name, field.name AS field_name
    #      FROM subfield 
    #      JOIN field ON subfield.field_id = field.name
    #      WHERE field.name = <field_filter>
    #      ORDER BY subfield.name;
    # SQL: SELECT problem.*, subfield.name AS subfield_name, field.name AS field_name
    #      FROM problem
    #      JOIN subfield ON problem.subfield_id = subfield.id
    #      JOIN field ON subfield.field_id = field.name
    #      WHERE subfield.id = <subfield_id> (or field.name = <field_name>)
    #      ORDER BY CASE 
    #          WHEN problem.severity = 'high' THEN 0
    #          WHEN problem.severity = 'medium' THEN 1
    #          WHEN problem.severity = 'low' THEN 2
    #      END;
    
    if not request.session.get('user_id'):
        return redirect('login')
    
    # Get all fields for dropdown
    fields = Field.objects.all()
    
    # Get subfields based on selected field
    subfields = []
    field_filter = request.GET.get('field')
    if field_filter:
        subfields = Subfield.objects.filter(field__name=field_filter)
    
    # Start with empty queryset
    problems = Problem.objects.none()
    searched = False
    
    # Apply filters if provided
    subfield_filter = request.GET.get('subfield')
    
    if field_filter:
        searched = True
        
        if subfield_filter:
            # Filter by specific subfield
            problems = Problem.objects.filter(subfield_id=subfield_filter)
        else:
            # Filter by field (all subfields in that field)
            problems = Problem.objects.filter(subfield__field__name=field_filter)
        
        # Order by severity: high -> medium -> low
        problems = problems.select_related('subfield', 'subfield__field').order_by(
            models.Case(
                models.When(severity='high', then=0),
                models.When(severity='medium', then=1),
                models.When(severity='low', then=2),
            )
        )
    
    context = {
        'fields': fields,
        'subfields': subfields,
        'problems': problems,
        'searched': searched,
    }
    return render(request, 'core/search_problems.html', context)


def problem_detail_view(request, problem_id):
    """Display problem details with researchers working on it"""
    # SQL: SELECT problem.*, subfield.name AS subfield_name, field.name AS field_name
    #      FROM problem
    #      JOIN subfield ON problem.subfield_id = subfield.id
    #      JOIN field ON subfield.field_id = field.name
    #      WHERE problem.id = <problem_id>;
    # SQL: SELECT project.*, user.name AS owner_name, user.institution
    #      FROM project
    #      JOIN user ON project.owner_id = user.id
    #      WHERE project.subfield_id = <problem_subfield_id>
    #      ORDER BY project.created_at DESC;
    # SQL: SELECT DISTINCT user.id, user.name, user.institution, user.rating
    #      FROM user
    #      JOIN project ON user.id = project.owner_id
    #      WHERE project.subfield_id = <problem_subfield_id>
    #      ORDER BY user.name;
    
    if not request.session.get('user_id'):
        return redirect('login')
    
    problem = get_object_or_404(Problem, id=problem_id)
    
    # Find researchers working on this problem
    # (researchers who have projects in the same subfield)
    related_projects = Project.objects.filter(
        subfield=problem.subfield
    ).select_related('owner')
    
    working_researchers = User.objects.filter(
        owned_projects__subfield=problem.subfield
    ).distinct()
    
    context = {
        'problem': problem,
        'working_researchers': working_researchers,
        'related_projects': related_projects,
    }
    return render(request, 'core/problem_detail.html', context)


# ==============================================================================
# FEATURE 5: CREATE & MANAGE PROJECTS
# ==============================================================================

def create_project_view(request):
    """Create a new project"""
    # SQL: SELECT name FROM field ORDER BY name;
    # SQL: SELECT subfield.id, subfield.name, field.name AS field_name
    #      FROM subfield
    #      JOIN field ON subfield.field_id = field.name
    #      ORDER BY field.name, subfield.name;
    # SQL: SELECT * FROM user WHERE user_type = 'researcher' AND id != <current_user_id>;
    # SQL: SELECT * FROM user WHERE id = <current_user_id>;
    # SQL: SELECT * FROM field WHERE name = <field_name>;
    # SQL: SELECT * FROM subfield WHERE id = <subfield_id>;
    # SQL: INSERT INTO project (title, description, owner_id, field_id, subfield_id, vacancy_status, created_at)
    #      VALUES (<title>, <description>, <owner_id>, <field_id>, <subfield_id>, <vacancy_status>, NOW());
    # SQL: INSERT INTO core_project_collaborators (project_id, user_id)
    #      VALUES (<project_id>, <collaborator_id>); -- for each selected collaborator
    
    if not request.session.get('user_id'):
        return redirect('login')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        field_name = request.POST.get('field')
        subfield_id = request.POST.get('subfield')
        vacancy_status = request.POST.get('vacancy_status') == 'true'
        collaborator_ids = request.POST.getlist('collaborators')
        
        user_id = request.session.get('user_id')
        user = get_object_or_404(User, id=user_id)
        field = get_object_or_404(Field, name=field_name)
        subfield = get_object_or_404(Subfield, id=subfield_id)
        
        project = Project.objects.create(
            title=title,
            description=description,
            owner=user,
            field=field,
            subfield=subfield,
            vacancy_status=vacancy_status
        )
        
        # Add selected collaborators to the project
        if collaborator_ids:
            for collab_id in collaborator_ids:
                if collab_id:
                    collaborator = User.objects.get(id=collab_id)
                    project.collaborators.add(collaborator)
        
        # Redirect to the user's profile to see the new project
        return redirect('profile', user_id=user.id)
    
    # GET request - show form
    fields = Field.objects.all()
    subfields = Subfield.objects.all().select_related('field')
    all_users = User.objects.filter(user_type='researcher').exclude(id=request.session.get('user_id'))
    
    context = {
        'fields': fields,
        'subfields': subfields,
        'all_users': all_users,
    }
    return render(request, 'core/create_project.html', context)


# ==============================================================================
# FEATURE 6: NOTIFICATIONS & COLLABORATION REQUESTS
# ==============================================================================

def notifications_view(request):
    """Display all collaboration requests"""
    # SQL: SELECT cr.*, sender.name AS sender_name, sender.institution, 
    #             project.title AS project_title, post.content AS post_content
    #      FROM collaboration_request cr
    #      JOIN user sender ON cr.sender_id = sender.id
    #      LEFT JOIN project ON cr.project_id = project.id
    #      LEFT JOIN post ON cr.post_id = post.id
    #      WHERE cr.receiver_id = <current_user_id> AND cr.status = 'pending'
    #      ORDER BY cr.created_at DESC;
    # SQL: (Same query with status = 'accepted')
    # SQL: (Same query with status = 'rejected')
    
    if not request.session.get('user_id'):
        return redirect('login')
    
    user_id = request.session.get('user_id')
    
    # Get pending, accepted, and rejected requests
    pending_requests = CollaborationRequest.objects.filter(
        receiver_id=user_id,
        status='pending'
    ).select_related('sender', 'project', 'post').order_by('-created_at')
    
    accepted_requests = CollaborationRequest.objects.filter(
        receiver_id=user_id,
        status='accepted'
    ).select_related('sender', 'project', 'post').order_by('-created_at')
    
    rejected_requests = CollaborationRequest.objects.filter(
        receiver_id=user_id,
        status='rejected'
    ).select_related('sender', 'project', 'post').order_by('-created_at')
    
    context = {
        'pending_requests': pending_requests,
        'accepted_requests': accepted_requests,
        'rejected_requests': rejected_requests,
    }
    return render(request, 'core/notifications.html', context)


def accept_collaboration_view(request, request_id):
    """Accept a collaboration request"""
    # SQL: SELECT * FROM collaboration_request WHERE id = <request_id>;
    # SQL: UPDATE collaboration_request SET status = 'accepted' WHERE id = <request_id>;
    # SQL: INSERT INTO core_project_collaborators (project_id, user_id)
    #      VALUES (<project_id>, <sender_id>); -- if project collaboration
    
    if not request.session.get('user_id'):
        return redirect('login')
    
    collab_request = get_object_or_404(CollaborationRequest, id=request_id)
    
    # Update status
    collab_request.status = 'accepted'
    collab_request.save()
    
    # If it's a project collaboration, add sender as collaborator
    if collab_request.project:
        collab_request.project.collaborators.add(collab_request.sender)
    
    return redirect('notifications')


def reject_collaboration_view(request, request_id):
    """Reject a collaboration request"""
    # SQL: SELECT * FROM collaboration_request WHERE id = <request_id>;
    # SQL: UPDATE collaboration_request SET status = 'rejected' WHERE id = <request_id>;
    
    if not request.session.get('user_id'):
        return redirect('login')
    
    collab_request = get_object_or_404(CollaborationRequest, id=request_id)
    
    # Update status
    collab_request.status = 'rejected'
    collab_request.save()
    
    return redirect('notifications')