# Foodly

Foodly
Foodly – a next-generation food delivery platform that ensures fair wages for workers while minimizing costs for customers through smart algorithms.

Table of Contents
Overview

Features

Architecture & Tech Stack

Setup & Installation

Usage

Contributing

License

Overview
Foodly is a fair and efficient food delivery platform designed to improve traditional delivery systems. Unlike conventional apps, Foodly ensures:

Minimum guaranteed wages for delivery workers

Optimized delivery costs for customers

Smart algorithmic routing and task assignment to balance fairness and efficiency

This project is a simulation version designed for academic purposes, demonstrating the potential of algorithm-driven fair delivery systems.

Features
Worker-friendly: Ensures fair wages with optimized task assignment

Customer-friendly: Reduces overall delivery costs

Algorithm-driven: Uses smart algorithms to match orders with delivery agents efficiently

Mobile app interface for users (React Native)

Admin panel for monitoring and management (Next.js)

Backend powered by Supabase

Architecture & Tech Stack
Frontend (Mobile App): React Native

Admin Panel (Web): Next.js

Backend: Supabase (PostgreSQL + Auth + API)

Algorithm Module: Python-based smart assignment engine

Simulation Mode: Allows testing the algorithm and app without real transactions

Setup & Installation
Prerequisites

Node.js ≥ 18

npm or yarn

Python ≥ 3.10 (for algorithm module)

Supabase account

Steps

Clone the repository:
git clone https://github.com/yourusername/foodly.git
cd foodly

Set up the backend:
cd backend
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
pip install -r requirements.txt

Configure Supabase:

Create a new Supabase project

Update .env with Supabase credentials

Set up the mobile app:
cd ../mobile
npm install
npx expo start

Set up the admin panel:
cd ../admin
npm install
npm run dev

Usage
Launch the mobile app to simulate user orders

Launch the admin panel to monitor delivery assignments

Run the algorithm module to test optimized worker assignments and cost reduction

Contributing
Contributions are welcome! Please follow these steps:

Fork the repo

Create a new branch (git checkout -b feature-name)

Commit your changes (git commit -m 'Add feature')

Push to the branch (git push origin feature-name)

Open a Pull Request

License
This project is licensed under the MIT License.
