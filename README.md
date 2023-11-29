# EduFlip

EduFlip is an interactive flashcard study application designed to make learning fun and efficient. Developed as a Unit 5 Django project at Base Camp Coding Academy, EduFlip offers a unique platform for users to create, share, and study with flashcards on various topics.

## Project Timeline
Project initiation: November 13, 2023

![GitHub last commit](https://img.shields.io/github/last-commit/jobyfoster/eduflip)


## Features
- **Flashcard Creation and Management:** Users can create their own flashcard sets with custom topics.
- **Interactive Studying:** Engage with flashcards in a user-friendly interface.
- **Social Learning:** Share flashcard sets with peers and study together.
- **Responsive Design:** Accessible on various devices, providing a seamless user experience.

## Technology Stack
- **Frontend:** HTML, CSS (Bootstrap), JavaScript
- **Backend:** Django (Python)
- **Database:** SQLite (development), PostgreSQL (production)

## Installation and Setup
To get EduFlip up and running on your local machine for development and testing purposes, follow these steps:

1. **Clone the Repository**
```sh
git clone https://github.com/jobyfoster/eduflip.git
cd eduflip
```

2. **Set Up a Virtual Environment** (Optional but recommended)
```sh
python -m venv venv
source venv/bin/activate # On Windows use `venv\Scripts\activate`
```

3. **Install Required Packages**
```sh
pip install -r requirements.txt
```

4. **Generate and Set Django Secret Key**

- Create a .env file in the root directory. (Where `manage.py` is located)

- Generate a new Django secret key. You can use an online Django secret key generator or run the following in a Python shell:
```sh
import secrets
print(secrets.token_urlsafe(50))
```

- Add the secret key to the .env file:

```sh
DJANGO_SECRET_KEY=your_generated_secret_key
```

- Ensure that python-dotenv is installed (it should be in your requirements.txt).
- In settings.py, import the secret key:
```sh
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
```
5. **Run Migrations**
```sh
python manage.py migrate
```

6. **Start the Development Server**
```sh
python manage.py runserver
```

7. **Open the Application**
- Go to `http://localhost:8000` in your web browser.

## Contributing
Contributions to EduFlip are always welcome. You can contribute in various ways such as submitting bug reports, proposing new features, or writing code for improvements.

1. **Fork the Repository**
2. **Create a New Branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit Your Changes** (`git commit -m 'Add some AmazingFeature'`)
4. **Push to the Branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**

## License
Distributed under the GNU General Public License. See `LICENSE` for more information.

## Acknowledgments
- Base Camp Coding Academy for providing guidance and learning resources.
- All contributors who helped in building and refining EduFlip.

## Contact
- Joby Foster - jobyjfoster@gmail.com
- Project Link: https://github.com/jobyfoster/eduflip

