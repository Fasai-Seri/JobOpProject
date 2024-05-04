# Job Opportunity Project
## Members
6441126126 Nipasri Wongsiridech (Yok)
6441133526 Pathompong Sriamorn (Smart)
6441178826 Fasai Serikijcharoen (Fasai)

## Contributions
Fasai
- Job Post Application Backend:
    - Develop models and implement file renaming functionality upon upload
    - Implement full functionality for the job post app, including creation, display, and editing features
    - Integrate a search bar to filter job posts based on keywords
    - Manage view accessibility by displaying warning messages where necessary
    - Generate a PDF file containing a list of applicants with attached resumes
    - Integrate APScheduler to automatically update job post statuses based on their assigned close dates
- Javascript:
    - Implement filters for job posts based on job type, related major, and job status

## Features
### Core functionalities
- Create, display, and edit job posts (employers and professors)
- Apply for job posts (students)
- Favorite job posts
- Follow companies
### Additional functionalities
- Upload pictures and files to the database and rename to a consistent format 
- Export applicants list as pdf files attached with uploaded resume
- Utilize APScheduler to run job updating job status by close date
  
## Setup

``` Shell
# clone repository
git clone https://github.com/Fasai-Seri/JobOpProject.git
cd sample-django-app

# create a virtual environment and activate
python -m venv .venv
./.venv/scripts/activate

# install packages
pip install -r requirements.txt
npm i

# runserver
python manage.py runserver
```

## Frameworks

- Django 5.0.1
- React 17.0.2
- JQuery 3.7.1
- Select2 4.1.0
- Boostrap 4.4.1
- Maplibre-gl 4.1.2
- Maptiler 1.2.0
- Font awesome 4.3.0
