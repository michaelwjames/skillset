---
name: architecture-analyzer
description: This skill should be used when users request a deep architectural analysis of a codebase, including technology stack, project structure, design patterns, database schemas, authentication/authorization systems, and key architectural decisions. It can also perform static analysis to suggest improvements.
---

# Architecture Analyzer

This skill provides a systematic workflow for conducting comprehensive architectural analysis of codebases.

## Purpose

This skill enables deep analysis of codebase architecture by examining:
- Project structure and organization
- Technology stack and dependencies
- Database design and relationships
- Design patterns and architectural decisions
- Authentication, authorization, and security systems
- API structure and endpoints
- Frontend architecture and state management
- Backend architecture and business logic
- Code quality and maintainability

## When to Use This Skill

Use this skill when:
- A user requests an architectural overview or deep analysis of a codebase
- Documentation of existing architecture is needed
- Understanding system design decisions is required
- Onboarding new developers to a complex codebase
- Planning major refactoring or feature additions
- Auditing code quality and architectural patterns
- A user asks for suggestions to improve a codebase

## Scripts

### `suggest_improvements.py`
Analyzes a Python codebase and suggests improvements based on cyclomatic complexity and maintainability index.

**Usage:**
```bash
python suggest_improvements.py <path_to_codebase>
```

## AI Agent Analysis Workflow

This workflow is designed for an AI agent to perform architectural analysis using its available tools.

### Step 1: High-Level Exploration

1.  **List Files Recursively:**
    *   Use `ls -R` to get a complete, recursive listing of all files and directories in the repository.
    *   Save this output to a file (e.g., `file_listing.txt`) for reference.
    *   From this listing, identify key files such as `package.json`, `requirements.txt`, `pom.xml`, `Dockerfile`, `docker-compose.yml`, and any files in directories named `config`, `database`, or `migrations`.

2.  **Read Key Configuration Files:**
    *   Read the contents of the dependency management files (`package.json`, `requirements.txt`, etc.) to identify the primary frameworks and libraries.
    *   Read any database configuration files to determine the database system and connection details.
    *   Read Docker-related files to understand the containerization setup.

### Step 2: Source Code Analysis

1.  **Identify Application Entry Points:**
    *   For a web application, search for files that listen on a port (e.g., `grep -r "app.listen" .`).
    *   For a standalone application, look for a `main` function or script (`grep -r "if __name__ == '__main__':" .` for Python).

2.  **Trace Code Paths:**
    *   Starting from an entry point, use `grep` to follow function calls and class instantiations to understand the high-level control flow.
    *   For example, if you find a route definition like `app.get('/users', UserController.getUsers)`, you would then search for the `UserController` class and its `getUsers` method.

3.  **Investigate Key Architectural Components:**
    *   **Models/Entities:** Use `grep` to find class definitions that appear to be data models (e.g., `grep -r "class User" .`).
    *   **Controllers/Views:** Look for files that handle incoming requests and outgoing responses.
    *   **Services/Business Logic:** Search for files that contain the core application logic, often found in directories named `services`, `lib`, or `app`.
    *   **Database Interactions:** Search for common database query methods (e.g., `grep -r ".find(" .`, `grep -r ".query(" .`, `grep -r "SELECT .* FROM" .`).

### Step 3: Synthesize and Document

1.  **Create a Markdown Document:**
    *   Start a new Markdown file (e.g., `ARCHITECTURE.md`).

2.  **Document Findings:**
    *   **Technology Stack:** Based on the configuration files, list the primary languages, frameworks, and libraries.
    *   **Directory Structure:** Use the file listing to create a summary of the important directories and their purposes.
    *   **Data Model:** Describe the main data entities and their relationships.
    *   **Control Flow:** Explain how a typical request flows through the application.
    *   **Architectural Patterns:** Based on your analysis, identify any architectural patterns in use (e.g., MVC, RESTful API, Microservices).

3.  **Suggest Improvements:**
    *   Run the `suggest_improvements.py` script on the codebase.
    *   Incorporate the script's output into a "Recommendations" section of your `ARCHITECTURE.md` file.

## Conceptual Analysis Workflow

### Phase 1: Project Discovery

1. **Identify the root directory structure**
   - List top-level directories to understand project organization
   - Identify frontend, backend, database, and configuration directories
   - Note any monorepo or multi-service architecture

2. **Analyze dependency files**
   - Backend: Check for `package.json`, `requirements.txt`, `composer.json`, `pom.xml`, `Gemfile`, etc.
   - Frontend: Check for `package.json`, `yarn.lock`, `pnpm-lock.yaml`
   - Document all major dependencies and frameworks

3. **Identify configuration files**
   - Environment configuration (`.env.example`, config files)
   - Build tools (`vite.config.js`, `webpack.config.js`, `tsconfig.json`)
   - Database configuration
   - Deployment configuration

### Phase 2: Backend Analysis

1. **Framework and architecture**
   - Identify the backend framework (Express, Laravel, Django, etc.)
   - Determine architectural pattern (MVC, Clean Architecture, Layered, etc.)
   - Map out the directory structure (controllers, models, services, routes)

2. **Database layer**
   - Locate migration files and analyze table structures
   - Identify relationships between entities
   - Document seeder files and initial data
   - Map out the data model and ER relationships

3. **API and routing**
   - Analyze route definitions
   - Document API endpoints and their purposes
   - Identify middleware and request processing flow
   - Note authentication/authorization mechanisms

4. **Business logic**
   - Identify service layers and business rules
   - Document validation schemas
   - Map out data transformation and processing

### Phase 3: Frontend Analysis

1. **Framework and structure**
   - Identify frontend framework (React, Vue, Angular, etc.)
   - Analyze component hierarchy and organization
   - Document page/route structure

2. **State management**
   - Identify state management solution (Redux, Zustand, Pinia, Context API)
   - Analyze store structure and state flow
   - Document data fetching patterns

3. **UI components**
   - Identify component library (shadcn/ui, Material UI, custom)
   - Document reusable component patterns
   - Note styling approach (Tailwind, CSS modules, styled-components)

4. **Client-side routing**
   - Map out route definitions
   - Document navigation patterns
   - Identify protected routes and auth guards

### Phase 4: Cross-Cutting Concerns

1. **Authentication and Authorization**
   - Document authentication strategy (JWT, sessions, OAuth)
   - Analyze role-based access control (RBAC) implementation
   - Map permission checking throughout the application

2. **Security**
   - Identify CORS configuration
   - Document input validation and sanitization
   - Note security middleware and practices

3. **Error handling**
   - Analyze error handling patterns
   - Document logging and monitoring

4. **Testing**
   - Identify test frameworks and structure
   - Document test coverage approach
   - Note integration and E2E test patterns

### Phase 5: Documentation Generation

Create a comprehensive architecture document including:

1. **Executive Summary**
   - Technology stack overview
   - High-level architecture description
   - Key architectural decisions

2. **Project Structure**
   - Directory tree with explanations
   - Module organization

3. **Technology Stack**
   - Backend frameworks and libraries
   - Frontend frameworks and libraries
   - Database and ORM
   - Build tools and deployment

4. **Database Architecture**
   - Entity-relationship diagram (textual or Mermaid)
   - Table descriptions
   - Key relationships and constraints

5. **API Documentation**
   - Endpoint listing with purposes
   - Authentication requirements
   - Request/response patterns

6. **Frontend Architecture**
   - Component hierarchy
   - State management patterns
   - Routing structure

7. **Authentication & Authorization**
   - Auth flow description
   - Role and permission system
   - Protected resource patterns

8. **Key Patterns and Conventions**
   - Code organization patterns
   - Naming conventions
   - Common utilities and helpers

9. **Workflows and Business Logic**
   - Major user flows
   - Complex business processes
   - Data transformation pipelines

10. **Recommendations**
    - Architectural strengths
    - Areas for improvement
    - Technical debt observations
    - **(Automated) Code Quality Suggestions** from `suggest_improvements.py`

## Best Practices

1. **Start broad, then narrow**: Begin with high-level structure before diving into details
2. **Follow the data**: Trace data flow from database through backend to frontend
3. **Use grep strategically**: Search for patterns like `export class`, `router.`, `CREATE TABLE`
4. **Read key files fully**: Don't skip important configuration and entry point files
5. **Document as you go**: Build the analysis document incrementally
6. **Note inconsistencies**: Highlight areas where patterns deviate
7. **Consider the user's goal**: Tailor depth and focus to what the user needs to understand
8. **Leverage automation**: Use the `suggest_improvements.py` script to get a quick overview of code quality.
