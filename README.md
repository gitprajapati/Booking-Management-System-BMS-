# Booking Management System (BMS)

This is a modern, multi-user web application built with Flask and VueJS that allows users to book show tickets. Administrators have the ability to manage theaters and shows, including details like name, rating, ticket price, capacity, and tags.

## Features

- **Theater and Show Management:** Admins can create, edit, and remove theaters and shows.
- **User Signup and Login:** Users can create accounts and log in to access the platform.
- **Show Search and Booking:** Users can search for shows and theaters based on location, tags, and book available tickets.
- **Daily Reminders & Monthly Entertainment Reports:** Automated emails remind users to book shows and provide monthly reports with booking details and show ratings.
- **User-Triggered Async Job (Export as CSV):** Admins can export theater details, bookings, and ratings to CSV files.
- **Performance Enhancement with Caching:** Redis is used to improve application performance and optimize API calls.
- **Dynamic Ticket Pricing:** Ticket prices can fluctuate based on show popularity and ratings.
- **Downloadable PDF Tickets:** Users can download PDF tickets for their booked shows.

## Technologies Used

- **Backend:** Flask, SQLAlchemy, Redis, Celery, Flask JWT
- **Frontend:** VueJS, Jinja2, Bootstrap
- **Database:** SQLite3

## Project Structure

```
ProjectFolder/
├── Project/
│   ├── API/
│   │   ├── auth/
│   │   │   ├── auth.py
│   │   │   └── role_selection.py
│   │   ├── admin/
│   │   │   ├── shows.py
│   │   │   └── venues.py
│   │   ├── user/
│   │   │   ├── rating.py
│   │   │   ├── search.py
│   │   │   ├── shows.py
│   │   │   └── venue.py
│   │   ├── static/
│   │   │   └── shows_image
│   │   ├── templates/
│   │   │   ├── daily_mail_temp.html
│   │   │   ├── monthly_mail_temp.html
│   │   │   └── ticketPDF.html
│   │   ├── app.py
│   │   ├── caching.py
│   │   ├── celery_worker.py
│   │   ├── config.py
│   │   ├── models.py
│   │   └── tasks.py
│   └── Frontend/
│       ├── node_modules/
│       ├── public/
│       │   └── src/
│       │       ├── assets/
│       │       │   └── images/
│       │       ├── components/
│       │       │   ├── admin_has_venue.vue
│       │       │   ├── admin_no_venue.vue
│       │       │   ├── adminNav.vue
│       │       │   └── navBar.vue
│       │       ├── mixins/
│       │       │   └── myMethods.js
│       │       └── router/
│       │           └── index.js
│       │       └── views/
│       │           ├── adminShows.vue
│       │           ├── Booking.vue
│       │           ├── HomeView.vue
│       │           ├── Login.vue
│       │           ├── Register.vue
│       │           ├── search.vue
│       │           ├── showDetails.vue
│       │           ├── showForm.vue
│       │           ├── userBooking.vue
│       │           └── venueForm.vue
│       ├── App.vue
│       ├── main.js
│       ├── index.html
│       ├── package.json
│       └── README.md
├── Project_doc.pdf
├── README.md
└── requirements.txt
└── api_yaml_file.yaml
```

## Database Schema Design

The database schema consists of the following tables:

- **venue:** Stores information about theaters (id, name, address, city, state, average venue rating, owner ID).
- **user:** Stores user data (id, first name, last name, email, username, password, creation timestamp, login timestamp, logout timestamp, account activity status).
- **token_blocklist:** Manages JWT token blacklisting (id, JWT ID, creation timestamp).
- **bookedticket:** Records booking details (id, first name, last name, user email, venue city, venue address, venue name, show name, booking date, number of seats, show ID).
- **show:** Stores show information (id, name, tag, start date, end date, image path, duration, average show rating, capacity, show date, caption, price, venue ID).
- **user_roles:** Manages user roles and permissions (id, user ID, role ID).
- **roles:** Defines different user roles (id, name).

## API Endpoints

The API endpoints are organized into the following directories:

- **auth/:** Handles user registration, login, and token-based authentication using Flask JWT.
- **admin/:** Provides endpoints for administrators to manage shows and venues (create, read, update, delete).
- **user/:** Includes endpoints for user interactions with shows, venues, and ratings.

## Running the Application

### Frontend

1. Navigate to the `Frontend` directory: `cd Frontend`
2. Install dependencies: `npm install`
3. Start the development server: `npm run dev`

### Backend

1. Create a virtual environment:
   ```bash
   python -m venv venv  # Use 'python3' if necessary
   ```
2. Activate the virtual environment:

   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```
     or
     ```bash
     source venv/Scripts/activate
     ```

     ```

3. Start the Redis server in a separate terminal: `redis-server`
4. Start the Celery beat process in another terminal: `celery -A main.celery beat --max-interval 1 -l info`
5. Start the Celery worker process in another terminal: `celery -A main.celery worker -l info`
6. Start Mailhog (for email testing) in another terminal: `mailhog` (accessible at `localhost:8025`)
7. Run the Flask application: `python app.py`

## Additional Information

- Refer to `Project_doc.pdf` for detailed project documentation.
- The `api_yaml_file.yaml` likely contains API specifications or documentation.

This enhanced README provides a more comprehensive overview of the project, including its features, technologies, structure, database schema, API endpoints, and instructions for running the application.
--- END OF FILE README.md ---
