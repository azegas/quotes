- [Quotes project](#quotes-project)
  - [The plan for quotes project](#the-plan-for-quotes-project)
    - [Phase 1: Foundation](#phase-1-foundation)
    - [Phase 2: Intermediate Challenges](#phase-2-intermediate-challenges)
    - [Phase 3: Advanced Challenges](#phase-3-advanced-challenges)
    - [Phase 4: Stretch Goals](#phase-4-stretch-goals)


# Quotes project

Fourth and last time me building such site. This time I will focus on utilizing [CBV's](https://docs.djangoproject.com/en/5.0/topics/class-based-views/) and [HTMX](https://htmx.org/).

## The plan for quotes project

- Code Quality: Use tools like flake8 or black to ensure your code is clean and follows Python best practices.
- Testing: Write tests for your Django models, views, and HTMX interactions. Learning to write good tests is crucial for development.
- Version Control: Make frequent commits and use branches to manage features or experiments. This is a good practice for any software development project.

This roadmap combines learning new technologies (HTMX, Docker, a JavaScript framework) with best practices in software development. Each phase builds upon the last, gradually increasing in complexity and helping you solidify your understanding of Django, class-based views, and beyond.

### Phase 1: Foundation

1. Setup Django Project
Initialize a new Django project and create a dedicated app for handling quotes.
2. Database Models
Design a Quote model in your Django app. Include fields like text, author, and source.
3. Class-Based Views
Implement basic CRUD (Create, Read, Update, Delete) functionality using Django's class-based views for your Quote model.

### Phase 2: Intermediate Challenges

4. Templates with HTMX
Start with Read functionality. Use HTMX to fetch and display quotes without a full page reload.
Gradually, implement Create, Update, and Delete functionalities using HTMX to make asynchronous requests to your Django views.
5. Advanced HTMX
Explore advanced HTMX features such as lazy loading, infinite scroll, or out-of-band updates to enhance user experience.
6. Search and Filtering
Implement a search feature to filter quotes by text or author. Use HTMX to dynamically display the search results without page refreshes.
7. User Authentication
Integrate Django's authentication system. Allow only authenticated users to create, update, or delete quotes.

### Phase 3: Advanced Challenges

8. REST API with Django REST Framework
Create a REST API for your quotes. This will be useful for phase 4, where you will integrate external applications or services.
9. Django Signals
Use Django signals to perform actions triggered by database changes. For example, log an action when a new quote is added or send a notification.
10. Dockerize Your Application
Learn about Docker and containerize your Django application. This will teach you about deployments and the importance of consistent development environments.

### Phase 4: Stretch Goals

11. JavaScript Frontend Framework
Choose a JavaScript framework (React, Vue, etc.) and use it to consume your REST API. This will challenge you to understand frontend development and API integration.
12. Continuous Integration/Continuous Deployment (CI/CD)
Implement CI/CD for your project using platforms like GitHub Actions, GitLab CI, or Jenkins. Automate testing and deployment processes.
13. Advanced Linux Server Management
Since you're working with Linux servers, challenge yourself to deploy your Dockerized application to a cloud server (AWS, DigitalOcean, etc.) manually. Then, automate the deployment process using Ansible or another automation tool.
