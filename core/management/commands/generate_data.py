from django.core.management.base import BaseCommand
from core.models import Field, Subfield, User, Problem, Project, Post, CollaborationRequest
import random

class Command(BaseCommand):
    help = 'Generate dummy data for the research platform'

    def handle(self, *args, **kwargs):
        self.stdout.write('🚀 Starting data generation...')
        
        # Clear existing data
        self.stdout.write('🗑️  Clearing existing data...')
        CollaborationRequest.objects.all().delete()
        Post.objects.all().delete()
        Project.objects.all().delete()
        Problem.objects.all().delete()
        Subfield.objects.all().delete()
        Field.objects.all().delete()
        User.objects.all().delete()
        
        # ===================================================================
        # 1. CREATE FIELDS
        # ===================================================================
        self.stdout.write('📚 Creating fields...')
        fields_data = [
            'Computer Science',
            'Biology',
            'Physics',
            'Chemistry',
            'Mathematics',
        ]
        fields = []
        for name in fields_data:
            field = Field.objects.create(name=name)
            fields.append(field)
        self.stdout.write(f'✅ Created {len(fields)} fields')
        
        # ===================================================================
        # 2. CREATE SUBFIELDS
        # ===================================================================
        self.stdout.write('📖 Creating subfields...')
        subfields_data = {
            'Computer Science': ['Machine Learning', 'Artificial Intelligence', 'Database Systems', 'Computer Networks', 'Cybersecurity'],
            'Biology': ['Genetics', 'Molecular Biology', 'Ecology', 'Microbiology', 'Biotechnology'],
            'Physics': ['Quantum Physics', 'Astrophysics', 'Nuclear Physics', 'Particle Physics', 'Thermodynamics'],
            'Chemistry': ['Organic Chemistry', 'Inorganic Chemistry', 'Physical Chemistry', 'Analytical Chemistry', 'Biochemistry'],
            'Mathematics': ['Algebra', 'Calculus', 'Statistics', 'Number Theory', 'Topology'],
        }
        subfields = []
        for field_name, subfield_list in subfields_data.items():
            field = Field.objects.get(name=field_name)
            for subfield_name in subfield_list:
                subfield = Subfield.objects.create(name=subfield_name, field=field)
                subfields.append(subfield)
        self.stdout.write(f'✅ Created {len(subfields)} subfields')
        
        # ===================================================================
        # 3. CREATE USERS
        # ===================================================================
        self.stdout.write('👥 Creating users...')
        users_data = [
            {'name': 'Dr. John Smith', 'email': 'john@mit.edu', 'user_type': 'researcher', 'institution': 'MIT', 'country': 'USA', 'field': 'Machine Learning', 'rating': 4.8},
            {'name': 'Dr. Sarah Johnson', 'email': 'sarah@stanford.edu', 'user_type': 'researcher', 'institution': 'Stanford University', 'country': 'USA', 'field': 'Artificial Intelligence', 'rating': 4.7},
            {'name': 'Prof. Ahmed Hassan', 'email': 'ahmed@oxford.ac.uk', 'user_type': 'researcher', 'institution': 'Oxford University', 'country': 'UK', 'field': 'Genetics', 'rating': 4.9},
            {'name': 'Dr. Maria Garcia', 'email': 'maria@barcelona.edu', 'user_type': 'researcher', 'institution': 'University of Barcelona', 'country': 'Spain', 'field': 'Quantum Physics', 'rating': 4.6},
            {'name': 'Dr. Wei Chen', 'email': 'wei@tsinghua.edu.cn', 'user_type': 'researcher', 'institution': 'Tsinghua University', 'country': 'China', 'field': 'Database Systems', 'rating': 4.5},
            {'name': 'Prof. Raj Kumar', 'email': 'raj@iit.ac.in', 'user_type': 'researcher', 'institution': 'IIT Delhi', 'country': 'India', 'field': 'Cybersecurity', 'rating': 4.7},
            {'name': 'Tech Innovators Fund', 'email': 'contact@techfund.org', 'user_type': 'funding_agency', 'institution': 'Tech Innovators Fund', 'country': 'USA', 'field': 'Technology', 'rating': 0.0},
            {'name': 'Global Research Foundation', 'email': 'info@globalresearch.org', 'user_type': 'funding_agency', 'institution': 'Global Research Foundation', 'country': 'Switzerland', 'field': 'Science', 'rating': 0.0},
        ]
        users = []
        for user_data in users_data:
            user = User.objects.create(**user_data)
            users.append(user)
        self.stdout.write(f'✅ Created {len(users)} users (6 researchers + 2 funding agencies)')
        
        # ===================================================================
        # 4. CREATE PROBLEMS
        # ===================================================================
        self.stdout.write('⚠️  Creating problems...')
        problems_data = [
            {'name': 'Climate Change Impact on Ecosystems', 'severity': 'high', 'subfield': 'Ecology', 'description': 'Understanding how climate change affects biodiversity and ecosystem services.', 'current_work': 'Several teams studying temperature effects', 'done_work': 'Published 50+ papers on species migration', 'gaps': 'Need more data on tropical ecosystems'},
            {'name': 'AI Bias in Healthcare Algorithms', 'severity': 'high', 'subfield': 'Artificial Intelligence', 'description': 'Addressing biases in AI systems used for medical diagnosis.', 'current_work': 'Testing fairness metrics', 'done_work': 'Identified bias in 3 major systems', 'gaps': 'Limited datasets from diverse populations'},
            {'name': 'Quantum Computing Error Correction', 'severity': 'medium', 'subfield': 'Quantum Physics', 'description': 'Developing robust error correction codes for quantum computers.', 'current_work': 'Testing new topological codes', 'done_work': 'Demonstrated 99% error reduction', 'gaps': 'Scalability to 1000+ qubits'},
            {'name': 'Database Security Vulnerabilities', 'severity': 'high', 'subfield': 'Database Systems', 'description': 'Identifying and patching SQL injection vulnerabilities.', 'current_work': 'Automated vulnerability scanning', 'done_work': 'Patched 200+ systems', 'gaps': 'Need real-time detection systems'},
            {'name': 'Cancer Gene Therapy Delivery', 'severity': 'medium', 'subfield': 'Genetics', 'description': 'Improving viral vectors for gene therapy delivery to cancer cells.', 'current_work': 'Testing AAV vectors', 'done_work': 'Successful in 5 cancer types', 'gaps': 'Immune response challenges'},
            {'name': 'Machine Learning Model Interpretability', 'severity': 'medium', 'subfield': 'Machine Learning', 'description': 'Making deep learning models more transparent and explainable.', 'current_work': 'Developing SHAP values', 'done_work': 'Created 3 visualization tools', 'gaps': 'Works only for small models'},
            {'name': 'Renewable Energy Storage', 'severity': 'high', 'subfield': 'Physical Chemistry', 'description': 'Developing efficient battery technologies for renewable energy.', 'current_work': 'Testing solid-state batteries', 'done_work': 'Improved capacity by 30%', 'gaps': 'Cost reduction needed'},
            {'name': 'Cybersecurity in IoT Devices', 'severity': 'high', 'subfield': 'Cybersecurity', 'description': 'Securing billions of connected IoT devices from attacks.', 'current_work': 'Implementing blockchain authentication', 'done_work': 'Secured 1M+ devices', 'gaps': 'Computational overhead too high'},
            {'name': 'Antibiotic Resistance Mechanisms', 'severity': 'high', 'subfield': 'Microbiology', 'description': 'Understanding how bacteria develop resistance to antibiotics.', 'current_work': 'Genome sequencing studies', 'done_work': 'Identified 20 resistance genes', 'gaps': 'Need faster detection methods'},
            {'name': 'Graph Neural Networks Optimization', 'severity': 'low', 'subfield': 'Machine Learning', 'description': 'Improving training speed and accuracy of GNNs.', 'current_work': 'Testing new aggregation functions', 'done_work': 'Reduced training time by 40%', 'gaps': 'Limited to small graphs'},
        ]
        problems = []
        for problem_data in problems_data:
            subfield_name = problem_data.pop('subfield')
            subfield = Subfield.objects.get(name=subfield_name)
            problem = Problem.objects.create(subfield=subfield, **problem_data)
            problems.append(problem)
        self.stdout.write(f'✅ Created {len(problems)} problems')
        
        # ===================================================================
        # 5. CREATE PROJECTS
        # ===================================================================
        self.stdout.write('📁 Creating projects...')
        researchers = [u for u in users if u.user_type == 'researcher']
        projects_data = [
            {'title': 'Deep Learning for Medical Imaging', 'description': 'Using CNNs to detect diseases from X-rays and MRI scans.', 'owner': researchers[0], 'field': 'Computer Science', 'subfield': 'Machine Learning', 'vacancy_status': True},
            {'title': 'CRISPR Gene Editing for Cancer', 'description': 'Developing precise CRISPR techniques for cancer treatment.', 'owner': researchers[2], 'field': 'Biology', 'subfield': 'Genetics', 'vacancy_status': True},
            {'title': 'Quantum Cryptography Protocol', 'description': 'Creating unbreakable encryption using quantum entanglement.', 'owner': researchers[3], 'field': 'Physics', 'subfield': 'Quantum Physics', 'vacancy_status': False},
            {'title': 'AI-Powered Cybersecurity System', 'description': 'Real-time threat detection using machine learning.', 'owner': researchers[5], 'field': 'Computer Science', 'subfield': 'Cybersecurity', 'vacancy_status': True},
            {'title': 'Distributed Database Optimization', 'description': 'Improving query performance in distributed systems.', 'owner': researchers[4], 'field': 'Computer Science', 'subfield': 'Database Systems', 'vacancy_status': False},
            {'title': 'Climate Modeling with AI', 'description': 'Using neural networks to predict climate patterns.', 'owner': researchers[1], 'field': 'Computer Science', 'subfield': 'Artificial Intelligence', 'vacancy_status': True},
        ]
        projects = []
        for project_data in projects_data:
            field_name = project_data.pop('field')
            subfield_name = project_data.pop('subfield')
            field = Field.objects.get(name=field_name)
            subfield = Subfield.objects.get(name=subfield_name, field=field)
            project = Project.objects.create(field=field, subfield=subfield, **project_data)
            projects.append(project)
        self.stdout.write(f'✅ Created {len(projects)} projects')
        
        # ===================================================================
        # 6. CREATE POSTS
        # ===================================================================
        self.stdout.write('📝 Creating posts...')
        posts_data = [
            {'author': researchers[0], 'content': 'Looking for collaborators on a new AI project focused on natural language processing. Anyone interested in transformer models?'},
            {'author': researchers[1], 'content': 'Just published our paper on reinforcement learning! Check it out and let me know your thoughts.'},
            {'author': researchers[2], 'content': 'Excited to announce we got funding for our gene therapy research! Looking for molecular biologists to join the team.'},
            {'author': researchers[3], 'content': 'Has anyone worked with quantum error correction codes? Would love to discuss implementation challenges.'},
            {'author': researchers[4], 'content': 'Our new database indexing algorithm reduced query time by 50%! Happy to share details with anyone interested.'},
            {'author': researchers[5], 'content': 'Presenting at the International Cybersecurity Conference next month. Let me know if you\'ll be there!'},
            {'author': researchers[0], 'content': 'Seeking feedback on our latest ML model architecture. Anyone available for a quick review?'},
            {'author': researchers[1], 'content': 'What are the best practices for handling imbalanced datasets in medical AI? Open to suggestions!'},
        ]
        posts = []
        for post_data in posts_data:
            post = Post.objects.create(**post_data)
            posts.append(post)
        self.stdout.write(f'✅ Created {len(posts)} posts')
        
        # ===================================================================
        # 7. CREATE COLLABORATION REQUESTS
        # ===================================================================
        self.stdout.write('🤝 Creating collaboration requests...')
        collab_requests = [
            {'sender': researchers[1], 'receiver': researchers[0], 'project': projects[0], 'status': 'pending'},
            {'sender': researchers[4], 'receiver': researchers[5], 'project': projects[3], 'status': 'pending'},
            {'sender': researchers[3], 'receiver': researchers[2], 'project': projects[1], 'status': 'accepted'},
        ]
        for collab_data in collab_requests:
            CollaborationRequest.objects.create(**collab_data)
        self.stdout.write(f'✅ Created {len(collab_requests)} collaboration requests')
        
        # ===================================================================
        # SUMMARY
        # ===================================================================
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('🎉 DATA GENERATION COMPLETE!'))
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write(f'📚 Fields: {len(fields)}')
        self.stdout.write(f'📖 Subfields: {len(subfields)}')
        self.stdout.write(f'👥 Users: {len(users)} (6 researchers + 2 funding agencies)')
        self.stdout.write(f'⚠️  Problems: {len(problems)}')
        self.stdout.write(f'📁 Projects: {len(projects)}')
        self.stdout.write(f'📝 Posts: {len(posts)}')
        self.stdout.write(f'🤝 Collaboration Requests: {len(collab_requests)}')
        self.stdout.write(self.style.SUCCESS('='*60))