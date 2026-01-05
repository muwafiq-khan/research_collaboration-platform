from django.db import models

"""
RESEARCH COLLABORATION PLATFORM - DATABASE MODELS
==================================================
This file defines all 7 database models with their relationships.

RELATIONSHIPS SUMMARY:
1. Field (1) → Subfield (N) - One field has many subfields
2. Subfield (1) → Problem (N) - One subfield has many problems
3. User (1) → Project (N) - One user owns many projects
4. User (M) ↔ Project (N) - Many users collaborate on many projects (M:N)
5. User (1) → Post (N) - One user creates many posts
6. User (1) → CollaborationRequest (N) - One user sends many requests
7. User (1) → CollaborationRequest (N) - One user receives many requests
8. Project (1) → CollaborationRequest (N) - One project has many requests
9. Post (1) → CollaborationRequest (N) - One post has many requests
10. Field (1) → Project (N) - One field has many projects
11. Subfield (1) → Project (N) - One subfield has many projects
"""

# ==============================================================================
# MODEL 1: FIELD
# ==============================================================================
class Field(models.Model):
    """
    Represents a broad research field (e.g., Computer Science, Biology)
    
    RELATIONSHIPS:
    - One Field has MANY Subfields (1:N)
    - One Field has MANY Projects (1:N)
    
    PARTICIPATION:
    - Partial participation in relationships (field may exist without subfields/projects)
    
    SQL: CREATE TABLE field (name VARCHAR(200) PRIMARY KEY);
    """
    # Primary Key
    name = models.CharField(max_length=200, primary_key=True)
    
    class Meta:
        db_table = 'field'
    
    def __str__(self):
        return self.name


# ==============================================================================
# MODEL 2: SUBFIELD
# ==============================================================================
class Subfield(models.Model):
    """
    Represents a specific subfield within a broader field
    
    RELATIONSHIPS:
    - Many Subfields belong to ONE Field (N:1)
    - One Subfield has MANY Problems (1:N)
    - One Subfield has MANY Projects (1:N)
    
    PARTICIPATION:
    - Total participation with Field (every subfield MUST belong to a field)
    - Partial participation with Problem and Project
    
    SQL: CREATE TABLE subfield (
           id INT AUTO_INCREMENT PRIMARY KEY,
           name VARCHAR(200),
           field_id VARCHAR(200),
           FOREIGN KEY (field_id) REFERENCES field(name) ON DELETE CASCADE
         );
    """
    # Attributes
    name = models.CharField(max_length=200)
    
    # RELATIONSHIP: Many Subfields → One Field (N:1)
    # Foreign Key: subfield.field_id → field.name
    field = models.ForeignKey(
        Field,
        on_delete=models.CASCADE,      # Delete subfields when field is deleted
        related_name='subfields'       # Access: field.subfields.all()
    )
    
    class Meta:
        db_table = 'subfield'
    
    def __str__(self):
        return f"{self.name} ({self.field.name})"


# ==============================================================================
# MODEL 3: USER
# ==============================================================================
class User(models.Model):
    """
    Represents a user (Researcher or Funding Agency)
    
    RELATIONSHIPS (as source):
    - One User OWNS many Projects (1:N) - as owner
    - One User COLLABORATES on many Projects (M:N) - as collaborator
    - One User CREATES many Posts (1:N)
    - One User SENDS many CollaborationRequests (1:N)
    - One User RECEIVES many CollaborationRequests (1:N)
    
    PARTICIPATION:
    - Partial participation in all relationships
    
    SQL: CREATE TABLE user (
           id INT AUTO_INCREMENT PRIMARY KEY,
           name VARCHAR(200),
           email VARCHAR(254) UNIQUE,
           user_type VARCHAR(20),
           institution VARCHAR(300),
           country VARCHAR(100),
           field VARCHAR(200),
           rating DECIMAL(3,1) DEFAULT 0.0
         );
    """
    USER_TYPE_CHOICES = [
        ('researcher', 'Researcher'),
        ('funding_agency', 'Funding Agency'),
    ]
    
    # Attributes
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='researcher')
    institution = models.CharField(max_length=300)
    country = models.CharField(max_length=100)
    field = models.CharField(max_length=200)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    
    class Meta:
        db_table = 'user'
    
    def __str__(self):
        return self.name


# ==============================================================================
# MODEL 4: PROBLEM
# ==============================================================================
class Problem(models.Model):
    """
    Represents a research problem in a specific subfield
    
    RELATIONSHIPS:
    - Many Problems belong to ONE Subfield (N:1)
    
    PARTICIPATION:
    - Total participation with Subfield (every problem MUST belong to a subfield)
    
    SEVERITY:
    - 'high' = 🔴 Red (Critical)
    - 'medium' = 🟡 Yellow (Moderate)
    - 'low' = 🟢 Green (Low priority)
    
    SQL: CREATE TABLE problem (
           id INT AUTO_INCREMENT PRIMARY KEY,
           name VARCHAR(300),
           description TEXT,
           severity VARCHAR(20),
           subfield_id INT,
           current_work TEXT,
           done_work TEXT,
           gaps TEXT,
           FOREIGN KEY (subfield_id) REFERENCES subfield(id) ON DELETE CASCADE
         );
    """
    SEVERITY_CHOICES = [
        ('high', 'High'),      # 🔴 Red
        ('medium', 'Medium'),  # 🟡 Yellow
        ('low', 'Low'),        # 🟢 Green
    ]
    
    # Attributes
    name = models.CharField(max_length=300)
    description = models.TextField()
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='medium')
    current_work = models.TextField(blank=True)
    done_work = models.TextField(blank=True)
    gaps = models.TextField(blank=True)
    
    # RELATIONSHIP: Many Problems → One Subfield (N:1)
    # Foreign Key: problem.subfield_id → subfield.id
    subfield = models.ForeignKey(
        Subfield,
        on_delete=models.CASCADE,
        related_name='problems'  # Access: subfield.problems.all()
    )
    
    class Meta:
        db_table = 'problem'
    
    def __str__(self):
        return self.name


# ==============================================================================
# MODEL 5: PROJECT
# ==============================================================================
class Project(models.Model):
    """
    Represents a research project
    
    RELATIONSHIPS:
    - Many Projects belong to ONE User (owner) (N:1)
    - Many Projects belong to ONE Field (N:1)
    - Many Projects belong to ONE Subfield (N:1)
    - Many Projects have MANY Users (collaborators) (M:N)
    - One Project has MANY CollaborationRequests (1:N)
    
    PARTICIPATION:
    - Total participation with owner, field, subfield
    - Partial participation with collaborators and requests
    
    VACANCY STATUS:
    - True = 🟢 Open (Accepting collaborators)
    - False = 🔴 Closed (Not accepting)
    
    SQL: CREATE TABLE project (
           id INT AUTO_INCREMENT PRIMARY KEY,
           title VARCHAR(300),
           description TEXT,
           owner_id INT,
           field_id VARCHAR(200),
           subfield_id INT,
           vacancy_status BOOLEAN DEFAULT TRUE,
           created_at DATETIME,
           FOREIGN KEY (owner_id) REFERENCES user(id) ON DELETE CASCADE,
           FOREIGN KEY (field_id) REFERENCES field(name) ON DELETE CASCADE,
           FOREIGN KEY (subfield_id) REFERENCES subfield(id) ON DELETE CASCADE
         );
         
         -- M:N Junction Table (auto-created by Django)
         CREATE TABLE core_project_collaborators (
           id INT AUTO_INCREMENT PRIMARY KEY,
           project_id INT,
           user_id INT,
           FOREIGN KEY (project_id) REFERENCES project(id) ON DELETE CASCADE,
           FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
         );
    """
    # Attributes
    title = models.CharField(max_length=300)
    description = models.TextField()
    vacancy_status = models.BooleanField(default=True)  # True=Open, False=Closed
    created_at = models.DateTimeField(auto_now_add=True)
    
    # RELATIONSHIP 1: Many Projects → One User (owner) (N:1)
    # Foreign Key: project.owner_id → user.id
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owned_projects'  # Access: user.owned_projects.all()
    )
    
    # RELATIONSHIP 2: Many Projects → One Field (N:1)
    # Foreign Key: project.field_id → field.name
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    
    # RELATIONSHIP 3: Many Projects → One Subfield (N:1)
    # Foreign Key: project.subfield_id → subfield.id
    subfield = models.ForeignKey(Subfield, on_delete=models.CASCADE)
    
    # RELATIONSHIP 4: Many Projects ↔ Many Users (M:N)
    # Creates junction table: core_project_collaborators
    # Junction table stores: (project_id, user_id) pairs
    collaborators = models.ManyToManyField(
        User,
        related_name='collaborated_projects',  # Access: user.collaborated_projects.all()
        blank=True
    )
    
    class Meta:
        db_table = 'project'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


# ==============================================================================
# MODEL 6: POST
# ==============================================================================
class Post(models.Model):
    """
    Represents a post in the world feed
    
    RELATIONSHIPS:
    - Many Posts belong to ONE User (author) (N:1)
    - One Post has MANY CollaborationRequests (1:N)
    
    PARTICIPATION:
    - Total participation with User (every post MUST have an author)
    - Partial participation with CollaborationRequest
    
    SQL: CREATE TABLE post (
           id INT AUTO_INCREMENT PRIMARY KEY,
           author_id INT,
           content TEXT,
           created_at DATETIME,
           FOREIGN KEY (author_id) REFERENCES user(id) ON DELETE CASCADE
         );
    """
    # Attributes
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    # RELATIONSHIP: Many Posts → One User (author) (N:1)
    # Foreign Key: post.author_id → user.id
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'  # Access: user.posts.all()
    )
    
    class Meta:
        db_table = 'post'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.author.name}: {self.content[:50]}"


# ==============================================================================
# MODEL 7: COLLABORATION REQUEST
# ==============================================================================
class CollaborationRequest(models.Model):
    """
    Represents a collaboration request between users
    
    RELATIONSHIPS:
    - Many Requests sent by ONE User (sender) (N:1)
    - Many Requests received by ONE User (receiver) (N:1)
    - Many Requests for ONE Project (N:1) - optional
    - Many Requests for ONE Post (N:1) - optional
    
    PARTICIPATION:
    - Total participation with sender and receiver
    - Partial participation with project and post
    - Disjoint: Request is for EITHER project OR post, not both
    
    STATUS:
    - 'pending': Waiting for response
    - 'accepted': Approved (sender becomes collaborator if project)
    - 'rejected': Declined
    
    SQL: CREATE TABLE collaboration_request (
           id INT AUTO_INCREMENT PRIMARY KEY,
           sender_id INT,
           receiver_id INT,
           project_id INT NULL,
           post_id INT NULL,
           status VARCHAR(20) DEFAULT 'pending',
           created_at DATETIME,
           FOREIGN KEY (sender_id) REFERENCES user(id) ON DELETE CASCADE,
           FOREIGN KEY (receiver_id) REFERENCES user(id) ON DELETE CASCADE,
           FOREIGN KEY (project_id) REFERENCES project(id) ON DELETE CASCADE,
           FOREIGN KEY (post_id) REFERENCES post(id) ON DELETE CASCADE
         );
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    
    # Attributes
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    # RELATIONSHIP 1: Many Requests → One User (sender) (N:1)
    # Foreign Key: collaboration_request.sender_id → user.id
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_requests'  # Access: user.sent_requests.all()
    )
    
    # RELATIONSHIP 2: Many Requests → One User (receiver) (N:1)
    # Foreign Key: collaboration_request.receiver_id → user.id
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_requests'  # Access: user.received_requests.all()
    )
    
    # RELATIONSHIP 3: Many Requests → One Project (N:1) - OPTIONAL
    # Foreign Key: collaboration_request.project_id → project.id
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    
    # RELATIONSHIP 4: Many Requests → One Post (N:1) - OPTIONAL
    # Foreign Key: collaboration_request.post_id → post.id
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    
    class Meta:
        db_table = 'collaboration_request'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.sender.name} → {self.receiver.name} ({self.status})"


"""
==============================================================================
COMPLETE RELATIONSHIPS SUMMARY
==============================================================================

1. Field (1) ──→ Subfield (N)
   Cardinality: 1:N
   Participation: Partial:Total
   Foreign Key: subfield.field_id → field.name

2. Subfield (1) ──→ Problem (N)
   Cardinality: 1:N
   Participation: Partial:Total
   Foreign Key: problem.subfield_id → subfield.id

3. User (1) ──→ Project (N) [owner]
   Cardinality: 1:N
   Participation: Partial:Total
   Foreign Key: project.owner_id → user.id

4. User (M) ↔ Project (N) [collaborators]
   Cardinality: M:N
   Participation: Partial:Partial
   Junction Table: core_project_collaborators(project_id, user_id)

5. User (1) ──→ Post (N)
   Cardinality: 1:N
   Participation: Partial:Total
   Foreign Key: post.author_id → user.id

6. User (1) ──→ CollaborationRequest (N) [sender]
   Cardinality: 1:N
   Participation: Partial:Total
   Foreign Key: collaboration_request.sender_id → user.id

7. User (1) ──→ CollaborationRequest (N) [receiver]
   Cardinality: 1:N
   Participation: Partial:Total
   Foreign Key: collaboration_request.receiver_id → user.id

8. Project (1) ──→ CollaborationRequest (N)
   Cardinality: 1:N
   Participation: Partial:Partial
   Foreign Key: collaboration_request.project_id → project.id

9. Post (1) ──→ CollaborationRequest (N)
   Cardinality: 1:N
   Participation: Partial:Partial
   Foreign Key: collaboration_request.post_id → post.id

10. Field (1) ──→ Project (N)
    Cardinality: 1:N
    Participation: Partial:Total
    Foreign Key: project.field_id → field.name

11. Subfield (1) ──→ Project (N)
    Cardinality: 1:N
    Participation: Partial:Total
    Foreign Key: project.subfield_id → subfield.id

==============================================================================
"""