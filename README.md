# Todo App - DevSecOps Project

Application de gestion de tâches déployée sur Kubernetes (k3s).

## Architecture
- **Frontend** : Flask + Jinja2 (port 5000)
- **Backend** : Flask REST API (port 5001)
- **Database** : PostgreSQL (port 5432)

## CI/CD
- GitHub Actions pour le build et push des images
- Déploiement automatisé sur k3s

## Auteur
Anas MEHRI - ESAIP 2026
