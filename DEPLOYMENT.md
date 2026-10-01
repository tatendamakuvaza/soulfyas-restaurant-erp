# Production Deployment Guide: Soulfyas Quality Restaurant ERP

This guide provides step-by-step instructions for deploying Soulfyas Quality Restaurant ERP to production on **Streamlit Community Cloud**, **Neon Cloud PostgreSQL**, **Docker**, and **Linux VPS**.

---

## 1. Deploy on Streamlit Community Cloud (Recommended & Instant)

Streamlit Community Cloud offers zero-cost, continuous deployment connected to your GitHub repository.

### Step 1: Push Code to GitHub
All updates and modules are already tracked on GitHub:
- Pull Request #1: `https://github.com/tatendamakuvaza/soulfyas-restaurant-erp/pull/1`

### Step 2: Connect Streamlit Cloud
1. Navigate to [share.streamlit.io](https://share.streamlit.io/) and log in with your GitHub account.
2. Click **Create app** > **Deploy a public/private app from GitHub**.
3. Select:
   - **Repository**: `tatendamakuvaza/soulfyas-restaurant-erp`
   - **Branch**: `main` (or `arena/01a0f75f-soulfyas-restaurant-erp`)
   - **Main file path**: `app.py`
   - **App URL**: `soulfyas-erp.streamlit.app` (or custom slug)
4. Click **Advanced settings...** > **Secrets** and add your production database URL (e.g. Neon PostgreSQL):
   ```toml
   DATABASE_URL = "postgresql+psycopg://username:password@ep-sample-pooler.neon.tech/soulfyas_db?sslmode=require"
   ```
   *(If you omit `DATABASE_URL`, the app automatically runs in self-contained SQLite mode with built-in seed data).*
5. Click **Deploy!**

---

## 2. Setting up Neon Cloud PostgreSQL (High-Availability Cloud Database)

1. Sign up for free at [neon.tech](https://neon.tech/).
2. Create a project named `soulfyas-restaurant-erp` and select the **Europe (Frankfurt)** or **Africa / South Africa** region for low latency to Zimbabwe.
3. In your Neon dashboard:
   - Copy the **Connection String** (Pooled connection mode).
   - Ensure the driver prefix is `postgresql+psycopg://` or standard `postgresql://`.
4. The ERP's `database.py` engine automatically detects PostgreSQL, initializes all normalized tables, and seeds the initial chart of accounts, users, and tax rates without needing manual SQL script runs.

---

## 3. Deploying with Docker & Docker Compose

For on-premise local server deployment at the restaurant or on cloud instances (AWS EC2, DigitalOcean Droplet, Linode):

```bash
# Clone the repository
git clone https://github.com/tatendamakuvaza/soulfyas-restaurant-erp.git
cd soulfyas-restaurant-erp

# Build and start container in detached mode
docker-compose up -d --build

# View container logs
docker-compose logs -f
```

The ERP will be available at `http://YOUR_SERVER_IP:8501`.

---

## 4. Production Security & Best Practices

1. **Replace Default Credentials**:
   - Immediately log in as `admin` / `ChangeMe123!`.
   - Go to **User Administration & RBAC**, create named accounts for managers and cashiers, and change the default admin password.
2. **Backups & Audit Logs**:
   - Enable automated point-in-time recovery (PITR) in Neon or daily cron SQLite backups.
   - All critical actions (POS sales, stock adjustments, journal postings, logins) are permanently recorded in the **Central System Audit Trail**.
3. **Statutory Tax Rates**:
   - Review and update statutory parameters under **Settings** & **ZIMRA Tax Hub** (VAT 15%, NSSA 4.5%, IMTT 2%) in line with current official gazettes.
