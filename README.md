# 🌱 Attendance Management System

## 📌 Overview

This **Attendance Management System** is built for **Gampaha Wickramarachchi University of Indigenous Medicine** to streamline the process of attendance tracking, fingerprint record management, leave date monitoring, and more for university staff and faculty members.

---

## ✨ Features

- ✅ **User authentication** and role-based access control
- 📅 **Attendance tracking** with fingerprint records
- 📝 **Admin review and approval** of attendance records
- 📊 **Leave date monitoring** and reporting
- 📢 **Notification system** for attendance updates
- 🗓 **Dashboard** for viewing attendance reports and leave details

---

## 🛠 Technologies Used

- **Frontend:** 🎨 HTML, CSS, JavaScript (React/Vue/Angular if applicable)
- **Backend:** ⚙️ Django/Node.js/Flask
- **Database:** 🐖 PostgreSQL/MySQL/Firebase Realtime Database
- **Authentication:** 🔐 Firebase Auth/Custom JWT Authentication

---

## 🚀 Installation

### 📌 Prerequisites

- 🐍 Python 3.x / 🌍 Node.js
- 👢 PostgreSQL/MySQL/Firebase setup
- 🏭 Virtual environment (for Python projects)

### 📦 Steps

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/attendance-management-system.git
   cd attendance-management-system
   ```
2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt  # For Python projects
   npm install  # For Node.js projects
   ```
3. **Set up the database:**
   - Update `.env` file with database credentials
   - Run migrations (if using Django):
     ```sh
     python manage.py migrate
     ```
4. **Start the server:**
   ```sh
   python manage.py runserver  # Django
   ```
5. **Access the application** at `http://localhost:8000/` or `http://localhost:3000/`

---

## 🚀 Creating an Executable (.exe) File

To easily run the application with one click, you can create an executable file (.exe) using **PyInstaller**. Follow the steps below:

### 📌 Prerequisites

- 🐍 Python 3.x
- 🏭 Virtual environment (for Python projects)
- **PyInstaller** (to create the .exe)
- **App icon** (app_icon.png for the executable)

### 📦 Steps to Create the Executable

1. **Clone the repository:**

   ```sh
   git clone https://github.com/yourusername/attendance-management-system.git
   cd attendance-management-system
   ```

2. **Install dependencies:**
   Install Python dependencies by running:

   ```sh
   pip install -r requirements.txt
   ```

3. **Run the `executable_creator.py` script**:

   To generate the `.exe` file, run:

   ```sh
   pyinstaller --onefile --noconsole --icon=app_icon.ico app.py
   ```

   This will package the project into an executable (`app.exe`) located in the `dist` folder. The `.exe` file will have the `app_icon.png` as the icon.

4. **Test the executable**:

   - Once the `.exe` file is generated, go to the `dist` folder and double-click the `app.exe` file.
   - It should:
     1. Activate the virtual environment.
     2. Navigate to the project folder.
     3. Run the `python manage.py runserver` command to start the Django development server.

5. **Manual Server Start (Optional)**:

   - If you prefer to manually start the Django server without using the `.exe` file, you can run the following command:

   ```sh
   python manage.py runserver
   ```

   - Visit the application at `http://localhost:8000/` in your browser.

---

## 📚 Usage

- 👤 **Users:** Login to check attendance records and leave details.
- 👨‍💼 **Admins:** Review and manage attendance and leave requests.
- 📊 **Dashboard:** View attendance statistics and reports.

---

## 🤝 Contribution

We welcome contributions! Follow these steps:

1. **Fork the repository.**
2. **Create a new branch:** `git checkout -b feature-branch`
3. **Commit changes:** `git commit -m "Add new feature"`
4. **Push to the branch:** `git push origin feature-branch`
5. **Open a pull request.**

---

## 📝 License

This project is licensed under the **Apache License**.

---

## 💌 Contact

For inquiries, contact **info.dev.udith@gmail.com** or open an issue in the repository.
