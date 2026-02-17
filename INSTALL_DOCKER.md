# 🐳 Install Docker to Run AI-DOS

## You Need Docker First!

AI-DOS runs in Docker containers. Here's how to install it:

---

## 📥 Step 1: Download Docker Desktop

**Go to:** https://www.docker.com/products/docker-desktop/

**Or direct download:** https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe

---

## 🔧 Step 2: Install Docker Desktop

1. **Run the installer** (Docker Desktop Installer.exe)
2. **Follow the installation wizard**
3. **Enable WSL 2** (if prompted - recommended)
4. **Restart your computer** when installation completes

---

## ✅ Step 3: Verify Installation

Open a new Command Prompt and run:

```bash
docker --version
```

You should see something like:
```
Docker version 24.0.7, build afdd53b
```

Also check Docker Compose:
```bash
docker-compose --version
```

You should see:
```
Docker Compose version v2.23.0
```

---

## 🚀 Step 4: Start Docker Desktop

1. **Open Docker Desktop** from Start Menu
2. **Wait for it to start** (whale icon in system tray)
3. **Ensure it says "Docker Desktop is running"**

---

## 🎯 Step 5: Now Run AI-DOS!

Once Docker is installed and running:

```bash
cd c:\Projects\Software\AI-DOS
scripts\setup.bat
docker-compose up -d
```

Wait 60 seconds, then visit: **http://localhost:8000/docs**

---

## 🐛 Troubleshooting

### "WSL 2 installation is incomplete"

1. Open PowerShell as Administrator
2. Run:
```powershell
wsl --install
```
3. Restart computer
4. Start Docker Desktop again

### "Docker Desktop requires Windows 10 version 2004 or higher"

Update Windows:
1. Settings → Update & Security → Windows Update
2. Check for updates
3. Install all updates
4. Restart

### "Virtualization is not enabled"

Enable in BIOS:
1. Restart computer
2. Enter BIOS (usually F2, F10, or Del during boot)
3. Find "Virtualization Technology" or "Intel VT-x" or "AMD-V"
4. Enable it
5. Save and exit

---

## ⚡ Alternative: Test Without Docker (Limited)

If you can't install Docker right now, you can test the services individually:

### Install Python

1. Download Python: https://www.python.org/downloads/
2. Install (check "Add to PATH")

### Test DataForge Service

```bash
cd c:\Projects\Software\AI-DOS\services\dataforge
pip install -r requirements.txt
python main.py
```

Visit: http://localhost:8000/docs

### Test ModelHub Service

```bash
cd c:\Projects\Software\AI-DOS\services\modelhub
pip install -r requirements.txt
python main.py
```

Visit: http://localhost:8000/docs

**Note:** Without Docker, you won't have databases, so some features won't work. But you can see the API documentation and structure!

---

## 📋 System Requirements

**Minimum:**
- Windows 10 64-bit: Pro, Enterprise, or Education (Build 19041 or higher)
- 4GB RAM
- BIOS-level hardware virtualization support

**Recommended:**
- Windows 11 or Windows 10 (latest version)
- 8GB+ RAM
- SSD storage

---

## 🎊 After Docker is Installed

Come back and run:

```bash
cd c:\Projects\Software\AI-DOS
scripts\setup.bat
docker-compose up -d
```

Then follow **TEST_NOW.md** to start testing AI-DOS!

---

## 💡 Quick Links

- **Docker Desktop Download**: https://www.docker.com/products/docker-desktop/
- **Docker Documentation**: https://docs.docker.com/desktop/install/windows-install/
- **WSL 2 Setup**: https://learn.microsoft.com/en-us/windows/wsl/install

---

**Once Docker is installed, AI-DOS will work perfectly!** 🚀
