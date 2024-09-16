# Job Opportunity Project

## Members

6441126126 Nipasri Wongsiridech (Yok)  
6441133526 Pathompong Sriamorn (Smart)  
6441178826 Fasai Serikijcharoen (Fasai)

## Contributions

### Fasai

- Job Post Application Backend:
  - Develop models and implement file renaming functionality upon upload
  - Implement full functionality for the job post app, including creation, display, and editing features
  - Integrate a search bar to filter job posts based on keywords
  - Manage view accessibility by displaying warning messages where necessary
  - Generate a PDF file containing a list of applicants with attached resumes
  - Integrate APScheduler to automatically update job post statuses based on their assigned close dates
- Javascript:
  - Implement filters for job posts based on job type, related major, and job status

### Yok

- User Profile Frontend and Backend:
  - Develop models to keep and use necessary information
  - Authenticate and assign different permission for each type of account, resulting in different display and accessibility
  - Implement full functionality for user profile, including creation, display, and editing features
  - Design user profile page and prefill with existing information
  - Apply logical data flow in user profile page (ex. Only allow employer to change their company once)
- Company Profile Frontend and Backend:
  - Develop models to keep and use necessary information
  - Implement full functionality for company profile, including creation, display, and editing features
  - Integrate map api to identify the exact location of the company
  - Design company page and prefill with existing information

### Smart

- Job Post Application Frontend:
  - Design and layout all pages related to job posts (HTML / CSS files), such as the All Posts page, the Following page, the Favorite page, the Create/Edit Post page, and the Warning page.
  - Design the display of each post as a card layout that presents a summary of the job information, including a displays page that show all the details of the job.
  - Integrate the various pages by creating buttons and links, and display certain features differently for specific user groups.
  - Create the "Favorite" and "Apply" features for each job post (involving backend work in this part).
  - Modify the layout.html file in the navbar section to enhance the display features.
- Javascript:
  - Change the favorite/unfavorite icon immediately when clicked, and ensure that posts without a favorite status do not appear on the Favorite page.
  - Change the applied/unapplied status immediately when clicked, and include a status label for posts that the student has applied.
  - Display the names of uploaded PDF files when creating a post, and allow the deletion of incorrectly uploaded files, as well as prevent the user from selecting past dates as Inactive dates.

  
## Features

### Core functionalities

- Create, display, and edit job posts
- Apply for job posts
- Favorite job posts
- Follow companies
- Create, display, and edit user profiles
- Create, display and edit company profiles

### Additional functionalities

- Implement functionality to upload pictures and files to the database, ensuring consistent renaming to a predefined format
- Export applicants list as PDF files, with resumes attached
- Utilize APScheduler to automate the process of updating job statuses based on their close dates
- Implement 3rd party map api to help locating company address

## Setup

```Shell
# clone repository
git clone https://github.com/Fasai-Seri/JobOpProject.git
cd JobOpProject

# Build and start the application using Docker Compose
docker-compose up --build

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
