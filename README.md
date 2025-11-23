**Personal Finance Manager (Streamlit App)**

A simple and powerful Personal Finance Manager built using Python, Streamlit, and SQLite.
This app allows users to track their income and expenses, visualize spending habits, and even predict future expenses using machine learning.
==Features
🔐 User Authentication
Secure Sign-up and Login
Passwords stored using SHA-256 hashing
Optional email collection

💰 Income & Expense Tracking
Add income entries with amount, source, and date
Add expense entries with category, note, and date
10 predefined categories (Food, Transport, Rent, etc.)

📊 Dashboard
Total Income & Expenses
Remaining Balance
Category-wise bar chart

🤖 AI Prediction
Predicts next month's estimated expense using:
Polynomial regression
Historical monthly spending data

🗂 Data Management
View all expenses in a table
Local SQLite database (finance.db)

🖥 Tech Stack
Streamlit (UI)
SQLite (Database)
Pandas (Data handling)
NumPy (Math)
Matplotlib & Streamlit charts (Plots)
Scikit-Learn (Prediction model)

📦 Installation
1️⃣ Clone the repository:
git clone [https://github.com/your-username/your-repo-name.git](https://github.com/Sudeep63/Personal-Finance-Manager/tree/main)
cd your-repo-name

2️⃣ Install dependencies:
pip install streamlit pandas numpy matplotlib scikit-learn

3️⃣ Run the app:
streamlit run streamlit_finance_manager.py

📁 Project Structure
📂 Personal-Finance-Manager
│── streamlit_finance_manager.py
│── finance.db                # Auto-created on first run
│── README.md
│── requirements.txt

📌 Requirements.txt

Add this file for easier setup:
streamlit
pandas
numpy
matplotlib
scikit-learn

🛠 Future Enhancements
Dark mode UI
Email notifications
Export data as Excel/CSV
Monthly budget alerts
Multiple language support
Pie chart & line graph visualizations
Full mobile responsive UI
✨ Screenshots (Optional)
![Dashboard Screenshot](<img width="1910" height="1037" alt="image" src="https://github.com/user-attachments/assets/8515ee95-370c-4c7b-8b4e-96726b06db40" />
.png)

🤝 Contributing

Pull requests are welcome!
For major changes, please open an issue first to discuss what you’d like to improve.
