<h1 align="center" id="title">AeroMark</h1>

<p align="center"><img width=70px height=70px src="https://i.ibb.co/3c9QZG9/bookmark-5.png" alt="project-image"></p>

<p id="description">AeroMark is a personalized web app for managing bookmarks that lets you easily Create View and Delete bookmarks. It offers Tag and Collection organization sorting options offline reading with PDFs and screenshots Chrome extension support and the ability to backup bookmarks in CSV format. It also provides basic authentication as well as the option to log in using Google or GitHub credentials.</p>

<h2>🚀 Demo</h2>

[https://poetic-falcon-fully.ngrok-free.app](https://poetic-falcon-fully.ngrok-free.app)

  
  
<h2>🧐 Features</h2>

Here're some of the project's best features:

*   ✨ Bookmark Management: Easily create view and delete bookmarks for seamless organization.
*   🏷️ Tag and Collection Organization: Categorize bookmarks using Tags and Collections for efficient arrangement.
*   🔀 Sorting Options: Choose from various sorting methods to quickly access your content.
*   📚 Offline Reading: Save bookmarks as PDFs and screenshots for reading without an internet connection.
*   🌐 Chrome Extension Support: Extend AeroMark's functionality with a user-friendly Chrome extension.
*   🔐 Authentication Choices: Enjoy flexible authentication including basic Google or GitHub login options.
*   📦 Backup and Restore: Keep your bookmarks secure with easy backup and restore in CSV format.
*   🎨 Sleek User Interface (UI): AeroMark presents a beautifully crafted User Interface that enhances both aesthetics and usability.
*   📱 Responsive Design: AeroMark's UI is carefully designed to be responsive and adaptive across different devices and screen sizes.

<h2>🛠️ Installation Steps:</h2>

<p>1. Clone the Repository: Open your terminal/command prompt and navigate to the directory where you want to store the project. Then run the following command to clone the repository:</p>

```
git clone https://github.com/adivaste/AeroMark.git
```

<p>2. Navigate to Project Directory: Change your current directory to the newly cloned AeroMark repository:</p>

```
cd AeroMark
```

<p>3. Set Up Virtual Environment (Optional but Recommended): It's a good practice to create a virtual environment for your project to manage dependencies. To create and activate a virtual environment run:</p>

```
python3 -m venv venv       # Create virtual environment
source venv/bin/activate  # Activate virtual environment (Linux/macOS)
venv\Scripts\activate     # Activate virtual environment (Windows)
```

<p>4. Install Dependencies: Install the required Python dependencies using pip:</p>

```
pip install -r requirements.txt
```

<p>5. Database Setup: AeroMark might require a database setup.</p>

```
python manage.py makemigrations
python manage.py migrate
```

<p>6. Run the Application: Once you've completed the above steps you can run the AeroMark application. Refer to the project's documentation for the specific command to start the application:</p>

```
python manage.py runserver
```

<p>7. Access the Application: Open your web browser and navigate to http://localhost:8000 (or the URL specified by the application) to access AeroMark.</p>

<h2>💻 Built with</h2>

Technologies used in the project:

*   Python
*   Django
*   HTML
*   CSS
*   JavaScript
*   Sqlite3
*   JWT
*   DRF (Django Rest Framework)
*   Tailwind
*   Flowbite
