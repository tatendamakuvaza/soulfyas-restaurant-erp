# GitHub and Streamlit deployment

## 1. Test locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

## 2. Create the GitHub repository

1. Sign in to GitHub.
2. Create a new repository, for example `soulfyas-restaurant-erp`.
3. Keep it private if the application contains business data or proprietary code.
4. Do not upload `.env`, `secrets.toml`, database files or passwords.

## 3. Upload the project

From this project folder:

```bash
git init
git add app.py requirements.txt README.md DEPLOYMENT.md database_schema.sql soulfyas_logo.png .gitignore .streamlit/config.toml
git commit -m "Initial Soulfyas Restaurant ERP"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/soulfyas-restaurant-erp.git
git push -u origin main
```

Replace `YOUR_USERNAME` and the repository name with your actual values.

## 4. Create a Neon PostgreSQL database

1. Create a Neon project.
2. Copy the pooled PostgreSQL connection string.
3. Run `database_schema.sql` in the Neon SQL editor or through a migration process.
4. Keep the connection string private.

Example format:

```text
postgresql://user:password@host/database?sslmode=require
```

The current application uses SQLite syntax in some prototype operations. Before production Neon use, replace SQLite-specific `INSERT OR REPLACE`, `INSERT OR IGNORE` and `lastrowid` operations with PostgreSQL-compatible upserts and `RETURNING id`. This is important for reliable production operation.

## 5. Deploy on Streamlit Community Cloud

1. Open https://share.streamlit.io/
2. Sign in with GitHub.
3. Select the repository.
4. Select branch `main`.
5. Set the main file to `app.py`.
6. Deploy.
7. Open the app settings and add a secret:

```toml
DATABASE_URL = "postgresql://user:password@host/database?sslmode=require"
```

8. Save and reboot the application.

## 6. First production security actions

- Change `admin / ChangeMe123!` immediately.
- Create named accounts for administrators and managers.
- Disable the default account after creating a replacement administrator.
- Keep the GitHub repository private until security review is complete.
- Never place database credentials inside `app.py`.
- Enable Neon backups and connection pooling.
- Use a separate database for testing and production.
- Have an accountant configure the chart of accounts, tax rates and IFRS reporting before using official reports.

## 7. Deploying updates

```bash
git add .
git commit -m "Describe the change"
git push
```

Streamlit Community Cloud will normally redeploy after the push.
