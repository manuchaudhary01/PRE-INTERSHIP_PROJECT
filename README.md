🧩 Mini Integration Platform
This project demonstrates a microservices-based integration platform consisting of:

- CRM API: Manages customer information.
- Inventory API: Manages welcome package dispatch.
- Integration Service: Periodically polls CRM API for new customers and triggers package dispatch via Inventory API.
- Test Suite: Unit tests for the integration logic using unittest and unittest.mock.

📁 Project Structure
mini-integration-platform/
├── crm_api.py                # CRM Flask API (port 5000)
├── inventory_api.py          # Inventory Flask API (port 5001)
├── integration_service.py    # Integration logic (polls and integrates)
├── test_integration_service.py  # Unit tests for integration service
├── README.md

📦 Installation
1. Clone the repository:
git clone https://github.com/yourusername/mini-integration-platform.git
cd mini-integration-platform

2. Create PostgreSQL Databases:
CREATE DATABASE CRM_DATA;
CREATE DATABASE INVENTORY_DATA;

3. Install dependencies:
pip install -r requirements.txt
Or manually install:
pip install Flask Flask-SQLAlchemy flasgger requests

4. 🚀 Running the Services
Mini Integration Platform_PROJECT\PRE-INTERSHIP_PROJECT>cd CRM_API
1. Start CRM API
python crm_api.py

📍 Runs on http://localhost:5000

🧪 Swagger Docs: http://localhost:5000/apidocs

2. Start Inventory API
Mini Integration Platform_PROJECT\PRE-INTERSHIP_PROJECT>cd INVENTORY_API  
python inventory_api.py

📍 Runs on http://localhost:5001

🧪 Swagger Docs: http://localhost:5001/apidocs

3. Start Integration Service
Mini Integration Platform_PROJECT\PRE-INTERSHIP_PROJECT>cd INTEGRATION_LOGIC
python integration_service.py

⏱ Polls CRM every 5 seconds

📦 Sends welcome packages via Inventory API

5. 🧪 Running Unit Tests
Mini Integration Platform_PROJECT\PRE-INTERSHIP_PROJECT\INTEGRATION_LOGIC
python test_integration_service.py

- All integration service methods are tested for:
- Successful customer fetch
- API failure/timeout handling
- Successful and failed package dispatch

🔄 Integration Logic
The integration_service.py polls the CRM API and for every new customer not yet processed, it triggers a POST request to the Inventory API.

- Error handling is built in for:
- Network failures
- API timeouts
- Unexpected status codes

✅ Features
Microservice architecture
- PostgreSQL-backed APIs
- Swagger documentation
- Fault-tolerant integration with retries
- Automated tests with mocking
