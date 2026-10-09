# Udaykiran Portfolio

A modern full-stack personal portfolio website built with **Angular**
and **FastAPI**, backed by **SQLite/SQLAlchemy** and deployed using
free-tier services.

The portfolio presents professional experience, skills, projects, and a
contact form through a responsive, dark, minimal interface with subtle
Matrix-inspired visual effects.

## Live Website

**Frontend:** https://udaykiran-portfolio-nine.vercel.app/

**Backend API:** https://udaykiran-portfolio-api.onrender.com/

**GitHub:** https://github.com/ASC11Uday/Udaykiran-Portfolio

**LinkedIn:** https://www.linkedin.com/in/udaykiran-pallanti/

------------------------------------------------------------------------

## Features

-   Responsive single-page portfolio
-   Angular standalone component architecture
-   FastAPI REST backend
-   SQLite database with SQLAlchemy ORM
-   Dynamic About, Experience, Projects, and Skills data
-   Contact form with Web3Forms email delivery
-   Reactive form validation
-   Project card flip interaction
-   Scroll-reveal animations
-   Custom cursor for fine-pointer devices
-   Subtle Matrix-style background animation
-   Loading/initialization screen
-   Responsive navigation with active-section detection
-   Scroll progress indicator
-   Custom favicon
-   Reduced-motion accessibility support
-   GitHub and LinkedIn profile links
-   Production deployment with Vercel + Render
-   GitHub-based automatic deployment workflow

------------------------------------------------------------------------

## Tech Stack

### Frontend

-   Angular
-   TypeScript
-   HTML5
-   SCSS
-   Angular Reactive Forms
-   RxJS
-   Angular HttpClient

### Backend

-   Python
-   FastAPI
-   SQLAlchemy
-   SQLite
-   Pydantic
-   Uvicorn
-   python-dotenv

### Contact / External Services

-   Web3Forms --- production contact-form email delivery
-   Render --- backend hosting
-   Vercel --- frontend hosting
-   GitHub --- source control and deployment integration

### Development Tools

-   Git
-   GitHub Desktop
-   VS Code
-   Postman
-   PowerShell

------------------------------------------------------------------------

## Project Architecture

``` text
Udaykiran-Portfolio/
│
├── frontend/
│   └── portfolio-ui/
│       ├── public/
│       │   └── favicon.svg
│       │
│       ├── src/
│       │   ├── app/
│       │   │   ├── components/
│       │   │   │   ├── navbar/
│       │   │   │   ├── hero/
│       │   │   │   ├── about/
│       │   │   │   ├── experience/
│       │   │   │   ├── projects/
│       │   │   │   ├── skills/
│       │   │   │   ├── contact/
│       │   │   │   ├── footer/
│       │   │   │   ├── loading-screen/
│       │   │   │   ├── custom-cursor/
│       │   │   │   └── matrix-background/
│       │   │   │
│       │   │   ├── services/
│       │   │   │   ├── about.service.ts
│       │   │   │   ├── experience.service.ts
│       │   │   │   ├── project.service.ts
│       │   │   │   ├── skill.service.ts
│       │   │   │   └── contact.service.ts
│       │   │   │
│       │   │   └── shared/
│       │   │       └── scroll-reveal.directive.ts
│       │   │
│       │   ├── environments/
│       │   │   ├── environment.ts
│       │   │   └── environment.prod.ts
│       │   │
│       │   ├── index.html
│       │   ├── main.ts
│       │   └── styles.scss
│       │
│       ├── angular.json
│       ├── package.json
│       └── tsconfig.json
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   └── models.py
│   │
│   ├── requirements.txt
│   ├── .env
│   └── portfolio.db
│
├── .gitignore
├── .python-version
└── README.md
```

> `venv/`, `.env`, `portfolio.db`, `node_modules/`, Angular build
> output, and other generated files are intentionally excluded from Git
> through `.gitignore`.

------------------------------------------------------------------------

## Backend API

The FastAPI backend exposes the following production endpoints:

  Method   Endpoint             Purpose
  -------- -------------------- -------------------------------------
  GET      `/`                  API health/welcome response
  GET      `/api/about`         Portfolio profile information
  GET      `/api/projects`      Project data
  GET      `/api/experiences`   Experience data
  GET      `/api/skills`        Skill-group data
  POST     `/api/contact`       Backend contact endpoint
  GET      `/api/contacts`      Development/testing contact records

The frontend uses the `/api/about`, `/api/projects`, `/api/experiences`,
and `/api/skills` endpoints to load portfolio content dynamically.

### Example API response

`GET /api/about`

``` json
{
  "name": "Udaykiran",
  "role": "Senior Associate Engineer",
  "skills": [
    "Angular",
    "Python",
    "FastAPI",
    "Spring Boot",
    "Automation",
    "AI/ML"
  ]
}
```

------------------------------------------------------------------------

## Database

The backend uses **SQLite** with **SQLAlchemy**.

### Main database models

-   `Contact`
-   `Project`
-   `Experience`
-   `SkillGroup`

The database is initialized automatically when the FastAPI application
starts.

The project table also contains:

-   `overview`
-   `contribution`
-   `highlights`

These fields are migrated when missing by the backend initialization
logic.

### Important

The SQLite database is local application data and is intentionally
ignored by Git:

``` text
*.db
*.sqlite
*.sqlite3
```

For production deployment, the current portfolio uses the free Render
environment and therefore should not be treated as a persistent
production database solution for important data.

------------------------------------------------------------------------

## Contact Form

The production Angular contact form uses **Web3Forms**.

### Production flow

``` text
Visitor
   │
   ▼
Angular Contact Form
   │
   ▼
Web3Forms API
   │
   ▼
Portfolio Email Inbox
```

The frontend sends:

-   Name
-   Email
-   Message
-   Subject
-   Sender name
-   Reply-to email

The Web3Forms access key is designed to be used from client-side
applications, so it is present in the Angular environment configuration.

### Important security rule

Never place private credentials such as:

-   Gmail App Passwords
-   SMTP passwords
-   API secrets
-   database passwords

inside Angular frontend files.

The old FastAPI SMTP contact implementation remains in the backend for
the backend endpoint, but the deployed Angular contact form uses
Web3Forms because Render's free web service does not support the
outbound SMTP workflow required by the original Gmail implementation.

------------------------------------------------------------------------

## Environment Configuration

### Frontend

The Angular environment contains:

``` typescript
export const environment = {
  production: true,
  apiUrl: 'https://udaykiran-portfolio-api.onrender.com/api',
  web3FormsAccessKey: 'YOUR_WEB3FORMS_ACCESS_KEY'
};
```

For local development, use the local API URL:

``` text
http://127.0.0.1:8000/api
```

Do not hard-code private backend credentials into frontend environment
files.

### Backend

Create:

``` text
backend/.env
```

with the backend variables required by the legacy/local SMTP contact
endpoint:

``` env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USERNAME=your-email@example.com
EMAIL_PASSWORD=your-app-password
EMAIL_TO=your-email@example.com
```

Do not commit `.env` to Git.

------------------------------------------------------------------------

## Local Development

### Prerequisites

Install:

-   Python 3.13
-   Node.js
-   npm
-   Git

The repository currently targets Python 3.13 through:

``` text
.python-version
```

### 1. Clone the repository

``` bash
git clone https://github.com/ASC11Uday/Udaykiran-Portfolio.git
cd Udaykiran-Portfolio
```

------------------------------------------------------------------------

## 2. Start the Backend

Move into the backend:

``` bash
cd backend
```

Create a virtual environment:

### Windows

``` powershell
python -m venv venv
```

Activate it:

``` powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

``` powershell
pip install -r requirements.txt
```

Start FastAPI:

``` powershell
uvicorn app.main:app --reload
```

The local API will normally be available at:

``` text
http://127.0.0.1:8000
```

FastAPI documentation:

``` text
http://127.0.0.1:8000/docs
```

------------------------------------------------------------------------

## 3. Start the Angular Frontend

Open another terminal.

Move to:

``` bash
cd frontend/portfolio-ui
```

Install dependencies:

``` bash
npm install
```

Start Angular:

``` bash
npm start
```

or:

``` bash
ng serve
```

The local frontend will normally be available at:

``` text
http://localhost:4200
```

------------------------------------------------------------------------

## 4. Local Frontend → Backend Connection

For local development, the Angular environment should point to:

``` text
http://127.0.0.1:8000/api
```

The FastAPI CORS configuration must allow the local Angular origin.

When the frontend is running, verify:

-   About data loads
-   Experience data loads
-   Projects data loads
-   Skills data loads
-   Contact form works

------------------------------------------------------------------------

## Production Deployment

The project uses two separate free hosting services.

``` text
GitHub
   │
   ├──────────────► Vercel
   │                 Angular Frontend
   │
   └──────────────► Render
                     FastAPI Backend
```

### Frontend --- Vercel

Project settings:

``` text
Framework: Angular
Root Directory: frontend/portfolio-ui
Build Command: automatic Angular build
Output Directory: dist/portfolio-ui/browser
```

The production Angular build generates:

``` text
dist/portfolio-ui/browser
```

Vercel serves the contents of this directory.

### Backend --- Render

Configuration:

``` text
Runtime: Python 3
Root Directory: backend
Build Command: pip install -r requirements.txt
Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
Plan: Free
```

Production API:

``` text
https://udaykiran-portfolio-api.onrender.com
```

------------------------------------------------------------------------

## Deployment Workflow

The repository is connected to both Vercel and Render.

After a change:

``` bash
git add .
git commit -m "Describe the change"
git push origin main
```

The connected deployment services automatically build the relevant
application.

### Typical workflow

``` text
Edit code
   │
   ▼
Test locally
   │
   ▼
Git add
   │
   ▼
Git commit
   │
   ▼
Git push origin main
   │
   ├──► Vercel deploys frontend
   │
   └──► Render deploys backend
```

Always verify the production site after a deployment.

------------------------------------------------------------------------

## Responsive Design

The interface was tested during development across desktop, tablet, and
mobile layouts, including narrow viewport sizes.

Responsive behavior includes:

-   Mobile navigation menu
-   Responsive project cards
-   Responsive contact form
-   Flexible typography
-   Mobile section spacing
-   Tablet layout adjustments
-   Narrow-screen project-card height adjustments
-   Horizontal overflow prevention

------------------------------------------------------------------------

## UI / Design Direction

The visual design follows a primarily professional/minimal style with
subtle Matrix-inspired elements.

### Design principles

-   Dark charcoal/black foundation
-   Muted green accent
-   Green used selectively rather than as constant neon
-   Minimal glass effects
-   Subtle Matrix background
-   Smooth scroll-reveal animations
-   Interactive project cards
-   Custom cursor on fine-pointer devices
-   Reduced-motion support

The Matrix effect is intentionally subtle so the portfolio remains
professional and readable.

------------------------------------------------------------------------

## Accessibility / UX Considerations

The project includes:

-   Semantic buttons and links
-   Form validation
-   Focus-visible outlines
-   Reduced-motion handling
-   Responsive layouts
-   `aria-label` support where needed
-   Keyboard-friendly interactive controls
-   External links opened with `target="_blank"` and
    `rel="noopener noreferrer"`

------------------------------------------------------------------------

## Git Ignore / Sensitive Files

The repository intentionally ignores:

``` text
.env
.env.*
venv/
.venv/
node_modules/
dist/
.angular/
*.db
*.sqlite
*.sqlite3
__pycache__/
*.py[cod]
```

Never remove these protections simply to make deployment easier.

------------------------------------------------------------------------

## Known Limitations

### Render free service

The backend is hosted on Render's free tier.

Free services can:

-   spin down after inactivity
-   take time to wake up on the first request
-   have usage/bandwidth limits
-   restart during platform operations

### SQLite

SQLite is suitable for this portfolio's current data requirements, but
it should not be considered a robust persistent production database for
high-volume or critical application data on an ephemeral/free hosting
environment.

### Project GitHub links

Individual project cards currently do not point to separate project
repositories. Their GitHub field is currently unset/`#` until dedicated
repository URLs are added.

### Web3Forms

The production contact form depends on Web3Forms' free-tier submission
allowance.

------------------------------------------------------------------------

## Future Improvements

Possible future enhancements:

-   Add individual GitHub repository links for each project
-   Add a custom domain
-   Add Open Graph/social sharing metadata
-   Add stronger SEO metadata
-   Add a production database if persistent dynamic data becomes
    necessary
-   Add project screenshots or live demos
-   Add analytics
-   Add automated tests for frontend and backend
-   Add CI/CD validation before deployment
-   Add API health monitoring
-   Improve backend architecture by separating routes, schemas,
    services, and database configuration

------------------------------------------------------------------------

## Project Author

**Udaykiran Pallanti**

Senior Associate Engineer

### Profiles

-   LinkedIn: https://www.linkedin.com/in/udaykiran-pallanti/
-   GitHub: https://github.com/ASC11Uday

------------------------------------------------------------------------

## License

This project is a personal portfolio application.

Unless otherwise stated, the source code, content, branding, and
portfolio material are intended for personal use and should not be
reused as another person's portfolio without permission.
