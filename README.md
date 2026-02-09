# 🚀 Custom Helpdesk Module (Odoo)

A fully customized **Helpdesk Management System** built using the Odoo framework.  
This module provides complete ticket lifecycle management including **SLA automation, ticket assignment, email integration, timesheet tracking, and billing support**.

---

## 📌 Overview

The Custom Helpdesk module helps organizations efficiently manage customer support tickets by providing automation, performance tracking, and service billing capabilities.

It is designed using Odoo ORM, messaging framework, and modular architecture to simulate **enterprise-level helpdesk functionality**.

---

## ✨ Features

### 🎫 Ticket Management
- Create and manage support tickets
- Multi-team support
- Ticket workflow with stage tracking
- Priority-based ticket sorting
- Customer integration

---

### 👥 Helpdesk Teams
- Multiple helpdesk teams
- Team member visibility control
- Manual or automatic ticket assignment
- Least workload assignment algorithm

---

### ⏱ SLA Management
- SLA policies per team
- SLA based on ticket priority
- Automatic SLA deadline calculation
- SLA workflow enforcement

---

### 📧 Email Integration
- Email alias creation for teams
- Automatic ticket creation from incoming emails
- Team-based communication channels

---

### 🕒 Timesheet Tracking
- Track employee time spent on tickets
- Billable and non-billable tracking
- Employee-based rate configuration

---

### 💰 Customer Billing
- Create invoices directly from timesheets
- Hourly rate billing support
- Integration with Odoo Accounting

---

### 💬 Communication
- Chatter integration
- Activity scheduling
- Internal ticket communication tracking

---

## 🏗 Module Structure

custom_helpdesk/
│
├── data/
│ └── stage_data.xml
│
├── models/
│ ├── ticket.py
│ ├── team.py
│ ├── stage.py
│ ├── sla.py
│ └── ticketTimesheet.py
│
├── views/
│ ├── ticket_views.xml
│ ├── team_views.xml
│ ├── sla_views.xml
│ ├── stage_views.xml
│ └── menu.xml
│
├── security/
│ ├── groups.xml
│ └── ir.model.access.csv
│
├── static/
│ └── description/
│ └── icon.png
│
├── manifest.py
└── init.py


## 🔄 Workflow

Customer Email / Manual Ticket Creation
↓
Ticket Created
↓
SLA Applied Automatically
↓
User Assignment (Manual / Auto)
↓
Work Progress + Timesheets
↓
Invoice Generated (Optional)
↓
Ticket Closed


## 🧠 Technical Highlights

- Odoo ORM-based implementation
- Mail thread and chatter integration
- Automatic SLA computation
- Email alias automation
- Workload-based ticket assignment
- Timesheet-to-invoice automation


## 🚀 Future Improvements

- SLA breach notifications
- Reporting dashboard
- Customer portal support
- Ticket analytics and performance metrics
- AI-based ticket classification

---

## 🤝 Contribution

Contributions and suggestions are welcome.

---

## ⭐ Support

If you like this project, consider giving it a ⭐ on GitHub.
