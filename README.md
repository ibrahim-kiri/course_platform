# Course Platform

A robust and modern course platform built with Django, Cloudinary, Django-HTMX, and Django-Tailwind. This platform allows users to browse, manage, and participate in courses with an engaging user interface and smooth functionality.

---

## Features

- **User Authentication**: Secure login and registration system.
- **Email Verification**: Users must verify their email to access course video content.
- **Course Management**: Add, edit, and view courses.
- **Media Integration**: Utilize Cloudinary for managing and serving images and videos.
- **Dynamic UI**: Powered by Django-HTMX for interactive, server-driven user experiences.
- **Responsive Design**: Tailwind CSS ensures a modern and mobile-friendly interface.

---

## Technologies Used

- **Backend**: Django (Python)
- **Frontend**: Django-Tailwind for styling and HTMX for dynamic interactions
- **Media Storage**: Cloudinary
- **Database**: SQLite (default), easily configurable for PostgreSQL or MySQL
- **Deployment**: Fully deployable to platforms like Heroku, AWS, or DigitalOcean

---

## Prerequisites

Ensure you have the following installed:

- Python 3.8+
- Node.js and npm
- pipenv or virtualenv (optional but recommended for managing Python dependencies)

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/course_platform.git
   cd course_platform
   ```

2. **Create and Activate Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Node.js Dependencies**:
   ```bash
   cd <tailwind_app_directory>
   npm install
   ```

5. **Set Up Environment Variables**:
   Create a `.env` file in the project root and add:
   ```env
   SECRET_KEY=your_secret_key
   DEBUG=True
   CLOUDINARY_URL=cloudinary://<api_key>:<api_secret>@<cloud_name>
   ```

6. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

7. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```

---

## Usage

1. **Admin Interface**:
   - Visit `http://127.0.0.1:8000/admin/` to manage courses and users.
   - Create an admin user with:
     ```bash
     python manage.py createsuperuser
     ```

2. **Email Verification**:
   - Upon registration, users will receive an email verification link.
   - Verified users can access course video content.

3. **Tailwind Development**:
   - Start the Tailwind watcher for CSS changes:
     ```bash
     python manage.py tailwind start
     ```

4. **HTMX Features**:
   - HTMX enables dynamic partial updates without full-page reloads.
   - Ensure your HTMX views return partial HTML snippets where required.

---

## Deployment

1. **Prepare for Production**:
   - Set `DEBUG=False` in `.env`.
   - Add your domain to `ALLOWED_HOSTS` in `settings.py`.

2. **Static Files**:
   - Build Tailwind CSS for production:
     ```bash
     python manage.py tailwind build
     ```
   - Collect static files:
     ```bash
     python manage.py collectstatic
     ```

3. **Configure Your Hosting Provider**:
   - Set up your preferred hosting platform and configure environment variables.
   - Ensure the database is properly configured for production (e.g., PostgreSQL).

---

## License

This project is licensed under the [MIT License](LICENSE).
