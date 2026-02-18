# Frequently Asked Questions (FAQ)

Got questions? We've got answers! 🎯

---

## 📋 Table of Contents

- [General Questions](#-general-questions)
- [Installation & Setup](#-installation--setup)
- [Usage & Features](#-usage--features)
- [Technical Questions](#-technical-questions)
- [Contributing](#-contributing)
- [Troubleshooting](#-troubleshooting)
- [Future Plans](#-future-plans)
- [Community & Support](#-community--support)

---

## 🌟 General Questions

### What is AI-DOS?

AI-DOS (AI Development Operating System) is a complete ML platform with 9 microservices that lets you build, deploy, and scale machine learning models in 30 seconds.

**Key Features:**
- Natural language ML pipeline generation (Magic Mode)
- Complete experiment tracking and model registry
- One-click deployment
- Team collaboration
- Auto-scaling
- Business intelligence & analytics

---

### Why should I use AI-DOS instead of MLflow, W&B, or SageMaker?

**AI-DOS advantages:**
- ✅ **Free** - $0 cost vs $50-$500+/month
- ✅ **Fast** - 5-minute setup vs 30min-2hours
- ✅ **Complete** - 9 services vs fragmented tools
- ✅ **Easy** - Natural language ML vs complex configs
- ✅ **Open Source** - Full control vs vendor lock-in

See [comparison table](README.md#-why-ai-dos-wins) in README.

---

### Is AI-DOS production-ready?

**Current Status (v1.7.0):**
- ✅ All 9 services working
- ✅ 100% test pass rate
- ✅ Complete documentation
- ✅ Enterprise governance
- ⚠️ Some features simulated (training, deployment)

**Production-ready for:**
- Experiment tracking
- Dataset management
- Team collaboration
- Analytics & monitoring

**Coming in v2.0 (Q3 2026):**
- Real model training
- Real deployment
- Kubernetes support

---

### Is AI-DOS really free?

**Yes!** AI-DOS is 100% open source (MIT License).

**Costs:**
- Software: $0
- Infrastructure: Your own hardware/cloud (Docker required)
- Future: Optional managed hosting (coming later)

---

### Who built AI-DOS?

AI-DOS was created by [@oladeji0909-hash](https://github.com/oladeji0909-hash) and is maintained by the open-source community.

See [CONTRIBUTORS.md](CONTRIBUTORS.md) for the full list.

---

## 🚀 Installation & Setup

### What are the requirements?

**Minimum:**
- Docker Desktop installed
- 8GB RAM
- 10GB disk space
- Ports 8000-8008 available

**Recommended:**
- 16GB RAM
- SSD storage
- Good internet connection

---

### How do I install AI-DOS?

**Quick Start:**
```bash
git clone https://github.com/oladeji0909-hash/AI-DOS.git
cd AI-DOS
docker-compose -f docker-compose-minimal.yml up -d
```

Wait 60 seconds, then visit http://localhost:8000/docs

See [GETTING_STARTED.md](GETTING_STARTED.md) for detailed instructions.

---

### Does it work on Windows/Mac/Linux?

**Yes!** AI-DOS works on all platforms that support Docker:
- ✅ Windows 10/11 (with WSL2)
- ✅ macOS (Intel & Apple Silicon)
- ✅ Linux (all major distros)

---

### How long does installation take?

**First time:** 5-10 minutes (Docker image downloads)
**Subsequent starts:** 30-60 seconds

---

### Can I run it without Docker?

Not recommended. Docker ensures:
- Consistent environment
- Easy setup
- All dependencies included
- Service isolation

Manual installation would require setting up 9 services + 5 databases individually.

---

## 💻 Usage & Features

### How do I use Magic Mode?

**Web Dashboard:**
1. Open `frontend/dashboard/index.html`
2. Type your request: "Build a sentiment analyzer"
3. Click "Create Pipeline"

**Python SDK:**
```python
from aidos import magic
result = magic("Build a sentiment analyzer")
```

**CLI:**
```bash
aidos magic "Build a sentiment analyzer"
```

---

### How do I track experiments?

**Python SDK:**
```python
from aidos import ModelHub

mh = ModelHub()
exp = mh.create_experiment("My Model", "Testing", "proj_1", "user_1")
mh.log_metrics(exp['id'], {"accuracy": 0.95})
```

**CLI:**
```bash
aidos experiment create "My Model" --project proj_1
```

---

### How do I deploy a model?

**Python SDK:**
```python
from aidos import Deploy

deploy = Deploy()
deployment = deploy.create("exp_123", "My API")
print(deployment['endpoint_url'])
```

**CLI:**
```bash
aidos deploy create exp_123 "My API"
```

---

### Can I use AI-DOS with my existing ML code?

**Yes!** AI-DOS integrates with:
- PyTorch
- TensorFlow
- scikit-learn
- Hugging Face
- Any Python ML library

Use ModelHub to track your experiments and Deploy to serve your models.

---

### Does AI-DOS support team collaboration?

**Yes!** Collaboration service includes:
- Teams & members
- Resource sharing
- Comments & discussions
- Activity feed
- Notifications

See [GETTING_STARTED.md](GETTING_STARTED.md#6-collaboration---team-workflows) for examples.

---

## 🔧 Technical Questions

### What's the architecture?

AI-DOS uses microservices architecture:
- 9 services (FastAPI)
- 5 databases (PostgreSQL, MongoDB, Redis, MinIO, RabbitMQ)
- Docker Compose orchestration
- REST APIs

See [architecture diagram](README.md#%EF%B8%8F-architecture) in README.

---

### What programming languages are supported?

**Backend:** Python (FastAPI)
**SDK:** Python
**CLI:** Python
**Future:** JavaScript/TypeScript SDK planned

---

### Can I extend AI-DOS with custom services?

**Yes!** AI-DOS is modular. You can:
- Add new microservices
- Extend existing services
- Create custom integrations
- Build plugins

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

### How does data persistence work?

**Current (v1.7.0):**
- In-memory storage
- Data resets on Docker restart

**Coming (v1.5.0 in roadmap):**
- PostgreSQL for structured data
- MongoDB for documents
- MinIO for files
- Persistent across restarts

---

### Is AI-DOS secure?

**Security features:**
- JWT authentication
- Role-based access control
- Password hashing
- CORS protection
- Security policy in place

See [SECURITY.md](SECURITY.md) for details.

---

### Can I use AI-DOS in production?

**Current:** Best for development, testing, and experiment tracking

**v2.0 (Q3 2026):** Production-ready with:
- Real training & deployment
- High availability
- Kubernetes support
- Enterprise features

---

## 🤝 Contributing

### How can I contribute?

**Many ways to help:**
- 💻 Write code
- 📝 Improve docs
- 🐛 Report bugs
- 💡 Suggest features
- 🌍 Build community
- 🔒 Report security issues

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

### I'm new to open source. Can I still contribute?

**Absolutely!** We welcome beginners.

**Good first contributions:**
- Fix typos in documentation
- Add code examples
- Report bugs
- Answer questions
- Share on social media

Look for issues labeled `good first issue`.

---

### How do I get my name in CONTRIBUTORS.md?

Make any contribution! Once merged:
- Your name gets added
- You're recognized in the community
- You're part of AI-DOS history

---

### Do you have a Code of Conduct?

**Yes!** See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)

**Key points:**
- Be respectful
- No harassment
- No malicious code
- Follow guidelines

---

## 🔧 Troubleshooting

### Services won't start

**Check:**
1. Docker is running
2. Ports 8000-8008 are available
3. You have 8GB+ RAM
4. Wait 60 seconds for startup

**Fix:**
```bash
docker-compose -f docker-compose-minimal.yml down
docker-compose -f docker-compose-minimal.yml up -d
```

---

### Port already in use

**Error:** "port is already allocated"

**Fix:**
```bash
# Windows: Find process using port
netstat -ano | findstr :8000

# Kill the process or change ports in docker-compose-minimal.yml
```

---

### Services show as unhealthy

**Wait 60 seconds** - Services need time to start

**Check logs:**
```bash
docker-compose -f docker-compose-minimal.yml logs -f
```

---

### SDK import error

**Error:** `ModuleNotFoundError: No module named 'aidos'`

**Fix:**
```bash
cd sdk/python
pip install -e .
```

---

### CORS errors in browser

**Fix:** All services have CORS enabled. Make sure you're:
- Opening HTML files directly (file://)
- Or using a local server

---

### Data disappeared after restart

**Expected behavior** - Data is in-memory in v1.7.0

**Coming in v1.5.0:** Persistent database storage

---

## 🔮 Future Plans

### What's coming next?

See [ROADMAP.md](ROADMAP.md) for complete plans.

**Highlights:**
- **v2.0 (Q3 2026):** Real training, deployment, Kubernetes
- **v3.0 (Q4 2026):** AutoML, AI-powered features
- **v4.0 (Q2 2027):** Enterprise features
- **v5.0 (Q3 2027):** Global scale

---

### Will AI-DOS always be free?

**Yes!** Core platform will always be open source and free.

**Future revenue (optional):**
- Managed hosting service
- Enterprise support
- Training & certification
- Marketplace transaction fees (10%)

---

### Can I request features?

**Absolutely!**
- Open an issue on [GitHub](https://github.com/oladeji0909-hash/AI-DOS/issues)
- Join [GitHub Discussions](https://github.com/oladeji0909-hash/AI-DOS/discussions)
- Vote on existing requests

---

### When will real training/deployment be available?

**Target:** v2.0 (Q3 2026)

**Includes:**
- Real model training (PyTorch, TensorFlow)
- Real deployment (containers, serving)
- Kubernetes support
- High availability

---

## 💬 Community & Support

### Where can I get help?

**Resources:**
- 📚 [Getting Started Guide](GETTING_STARTED.md)
- 📖 [Documentation](README.md)
- 🐛 [GitHub Issues](https://github.com/oladeji0909-hash/AI-DOS/issues)
- 💬 Discord (coming soon)
- 📧 Email: team@ai-dos.io

---

### How do I report bugs?

1. Check if already reported in [Issues](https://github.com/oladeji0909-hash/AI-DOS/issues)
2. Create new issue with:
   - Clear description
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details

---

### How do I report security vulnerabilities?

**DO NOT** create public issues!

**Email:** security@ai-dos.io

See [SECURITY.md](SECURITY.md) for details.

---

### Is there a Discord/Slack community?

**Coming soon!** We're planning to launch:
- Discord server
- Community forums
- Regular meetups

Follow [@ai_dos](https://twitter.com/ai_dos) for updates.

---

### Can I use AI-DOS for commercial projects?

**Yes!** MIT License allows:
- Commercial use
- Modification
- Distribution
- Private use

**Requirements:**
- Include original license
- Include copyright notice

See [LICENSE](LICENSE) for details.

---

### How can I stay updated?

**Follow us:**
- ⭐ Star on [GitHub](https://github.com/oladeji0909-hash/AI-DOS)
- 🐦 Twitter: [@ai_dos](https://twitter.com/ai_dos)
- 💼 LinkedIn: [AI-DOS](https://linkedin.com)
- 📧 Email: team@ai-dos.io

**Check:**
- [CHANGELOG.md](CHANGELOG.md) - Release history
- [ROADMAP.md](ROADMAP.md) - Future plans
- [GitHub Releases](https://github.com/oladeji0909-hash/AI-DOS/releases)

---

## ❓ Still Have Questions?

**Didn't find your answer?**

- 💬 [Ask on GitHub Discussions](https://github.com/oladeji0909-hash/AI-DOS/discussions)
- 🐛 [Open an Issue](https://github.com/oladeji0909-hash/AI-DOS/issues)
- 📧 Email: team@ai-dos.io

**We're here to help!** 🤝

---

<div align="center">

**[Back to README](README.md)** • **[Getting Started](GETTING_STARTED.md)** • **[Contributing](CONTRIBUTING.md)**

Made with 🔥 by the AI-DOS community

</div>
