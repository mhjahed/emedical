✅ If Your Project Already Exists on Your Computer
1️⃣ Open Terminal / PowerShell

Go to your project folder:

cd path/to/your/project

Example:

cd C:\Users\Jahed\Pictures\Projects\emedical
2️⃣ Initialize Git (if not already initialized)
git init
3️⃣ Add All Files
git add .
4️⃣ Commit Files
git commit -m "Initial project upload"

If you get identity error, run this first:

git config --global user.name "Jahed"
git config --global user.email "your_email@example.com"
5️⃣ Connect to Your GitHub Repository
git remote add origin https://github.com/mhjahed/emedical.git

If it says remote already exists:

git remote remove origin
git remote add origin https://github.com/mhjahed/emedical.git
6️⃣ Set Main Branch
git branch -M main
7️⃣ Push to GitHub 🚀
git push -u origin main

If it asks for login:

Use your GitHub username

Use Personal Access Token (NOT password)

✅ If GitHub Shows README Already (Important)

If you created README directly on GitHub, you might see:

rejected because the remote contains work that you do not have locally

Then run:

git pull origin main --allow-unrelated-histories

Resolve any merge conflict if asked, then:

git push -u origin main
🔥 Quick Checklist

✔ You are inside project folder
✔ git init done
✔ git add .
✔ git commit
✔ git remote add origin
✔ git push -u origin main