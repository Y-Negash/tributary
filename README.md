# tributary

## Backend for Ford's Sensor Streaming System
This repository contains the backend infrastructure for Ford's sensor streaming system. The core is a Flask server that interacts with a Redis database to manage sensor data.

### Features:
"/record" Endpoint:
- Called regularly by vehicle-embedded sensors to submit data to the database.

"/collect" Endpoint:
- Allows the user-facing mobile application to fetch the stored sensor data.
