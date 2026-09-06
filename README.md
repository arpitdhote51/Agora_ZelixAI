# Rahul-ZelixAI Sales Agent

Rahul-ZelixAI Sales Agent is an AI-powered voice sales agent built with Agora Voice AI and Model Context Protocol (MCP).

The system enables the voice agent to retrieve student information from Google Sheets, conduct a sales conversation, record the call outcome, and trigger a WhatsApp follow-up.

## Architecture

```text
                    ┌──────────────────────┐
                    │   Agora Voice Agent  │
                    │        Rahul         │
                    └──────────┬───────────┘
                               │
                               │ MCP
                               ▼
                    ┌──────────────────────┐
                    │     MCP Server       │
                    │   Python + FastMCP   │
                    └──────────┬───────────┘
                               │
                    ┌──────────┴──────────┐
                    │                     │
                    ▼                     ▼
           ┌─────────────────┐   ┌─────────────────┐
           │ Google Apps     │   │   WhatsApp API  │
           │ Script          │   │   Follow-up     │
           └────────┬────────┘   └─────────────────┘
                    │
                    ▼
           ┌─────────────────┐
           │ Google Sheets   │
           │ Student Data    │
           └─────────────────┘
```

## Features

- Real-time AI voice conversations
- Student information lookup
- Lead qualification
- Call outcome tracking
- Google Sheets integration
- Automated WhatsApp follow-ups
- MCP-based tool integration
- Local MCP server
- Cloudflare Tunnel support
- No Google Cloud Service Account required
- Extensible architecture for CRM and other business systems

## Technology Stack

| Component | Technology |
|---|---|
| Voice AI | Agora |
| AI Agent | Rahul |
| Agent Protocol | MCP |
| MCP Framework | FastMCP |
| Backend | Python |
| Student Database | Google Sheets |
| Integration Layer | Google Apps Script |
| Messaging | WhatsApp Cloud API |
| Tunnel | Cloudflare Tunnel |
| Configuration | python-dotenv |

## Project Structure

```text
Rahul-ZelixAI-Sales-Agent/
│
├── server.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## MCP Tools

### `get_student(phone)`

Retrieves student information from Google Sheets using the student's phone number.

Example:

```text
get_student("919XXXXXXXXX")
```

Example response:

```json
{
  "success": true,
  "student": {
    "name": "Rahul",
    "course": "Data Science",
    "status": "Interested"
  }
}
```

### `complete_call(phone, outcome)`

Updates the student's call status and records the call outcome.

Example:

```text
complete_call(
    phone="919XXXXXXXXX",
    outcome="Interested - wants demo"
)
```

### `send_whatsapp(phone, name, course)`

Sends a follow-up WhatsApp message to the student.

Example:

```text
send_whatsapp(
    phone="919XXXXXXXXX",
    name="Rahul",
    course="Data Science"
)
```

Example message:

```text
Hi Rahul,

Thank you for speaking with us.

As discussed, here are the details for our Data Science program.

Our team will get in touch with you shortly.

Regards,
ZelixAI
```

### `complete_student_followup(phone, outcome)`

Orchestrates the complete post-call workflow.

```text
Call Completed
      │
      ▼
Identify Student
      │
      ▼
Update Call Outcome
      │
      ▼
Prepare Follow-up
      │
      ▼
Send WhatsApp
```

## Google Sheets

The Google Sheet stores student information.

Recommended columns:

```text
phone
name
course
status
call_status
call_outcome
```

Example:

| phone | name | course | status | call_status | call_outcome |
|---|---|---|---|---|---|
| 919XXXXXXXXX | Rahul | Data Science | Interested | Completed | Wants demo |
| 919XXXXXXXXX | Priya | AI Agents | New | Pending | |
| 919XXXXXXXXX | Amit | Machine Learning | Follow-up | Completed | Call later |

## Google Apps Script

Google Apps Script acts as the integration layer between the MCP server and Google Sheets.

```text
MCP Server
     │
     ▼
Google Apps Script
     │
     ▼
Google Sheets
```

It handles:

- Student lookup
- Student updates
- Call status updates
- Phone number normalization
- JSON responses

## Environment Variables

Create a `.env` file:

```env
GOOGLE_SCRIPT_URL=https://script.google.com/macros/s/YOUR_SCRIPT_ID/exec

WHATSAPP_TOKEN=your_whatsapp_access_token

WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id
```

Never commit `.env` or API credentials to GitHub.

Add the following to `.gitignore`:

```gitignore
.env
venv/
__pycache__/
*.pyc
```

## Installation

### 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd Rahul-ZelixAI-Sales-Agent
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv venv
venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

The project uses the MCP 1.x SDK.

If required:

```bash
python -m pip uninstall mcp -y
python -m pip install "mcp<2"
```

Verify the MCP version:

```bash
python -c "import mcp; print(mcp.__version__)"
```

## Running the MCP Server

Start the server:

```powershell
python server.py
```

The local server runs on:

```text
http://127.0.0.1:8000
```

MCP endpoint:

```text
http://127.0.0.1:8000/mcp
```

## Cloudflare Tunnel

To expose the local MCP server to Agora:

```powershell
cloudflared tunnel --url http://127.0.0.1:8000
```

Cloudflare will provide a public URL similar to:

```text
https://your-random-name.trycloudflare.com
```

The MCP endpoint becomes:

```text
https://your-random-name.trycloudflare.com/mcp
```

> Quick Tunnel URLs are temporary and may change when the tunnel is restarted.

## Agora Configuration

Configure the MCP server inside the Agora Voice Agent.

### MCP Server Name

```text
Zelxai
```

### Server URL

```text
https://your-random-name.trycloudflare.com/mcp
```

### Protocol

```text
Streamable HTTP
```

### Timeout

```text
10000 ms
```

## Voice Agent Workflow

```text
                    Student Calls
                         │
                         ▼
                ┌─────────────────┐
                │   Agora Agent   │
                │      Rahul      │
                └────────┬────────┘
                         │
                         ▼
                 Ask Phone Number
                         │
                         ▼
                  get_student()
                         │
                         ▼
              Retrieve Student Data
                         │
                         ▼
                 Sales Conversation
                         │
                         ▼
                 Handle Objections
                         │
                         ▼
                Qualify Student Lead
                         │
                         ▼
                 complete_call()
                         │
                         ▼
                Update Google Sheet
                         │
                         ▼
                 send_whatsapp()
                         │
                         ▼
                Student Follow-up
```

## Lead Qualification

The agent can classify leads based on the conversation.

Example categories:

```text
HOT
WARM
COLD
FOLLOW-UP
NOT INTERESTED
```

Example:

```text
Student:
"I'm interested, but I want to speak with my parents first."

Agent:
Lead Status → WARM
Follow-up → Required
```

## Example Conversation

```text
Rahul:
Hi, I'm calling from ZelixAI.
I wanted to understand if you're currently
looking for any courses in AI or Data Science.

Student:
Yes, I'm interested in Data Science.

Rahul:
Great. Could you share your phone number
so I can check your existing details?

Student:
919XXXXXXXXX

Rahul:
Let me quickly check that for you.

        ↓

      MCP

        ↓

get_student("919XXXXXXXXX")

        ↓

Student information retrieved

        ↓

Rahul continues the conversation...

        ↓

Student:
I'd like to attend a demo.

        ↓

complete_call()

        ↓

Google Sheet Updated

        ↓

send_whatsapp()

        ↓

WhatsApp Follow-up Sent
```

## Security

The voice agent does not directly access Google Sheets or WhatsApp.

Instead, the MCP server provides controlled tools:

```text
                  AI Agent
                     │
                     ▼
                MCP Server
                     │
          ┌──────────┴──────────┐
          ▼                     ▼
     Google Sheets          WhatsApp
```

Recommended production security measures:

- HTTPS for external communication
- Authentication for MCP endpoints
- API key/token validation
- Environment-based secret management
- Request validation
- Rate limiting
- Logging and monitoring
- Restricted allowed hosts and origins
- Secure WhatsApp credentials
- Persistent Cloudflare Tunnel instead of Quick Tunnel

## Troubleshooting

### MCP package error

Check the installed version:

```bash
python -c "import mcp; print(mcp.__version__)"
```

Install MCP 1.x:

```bash
python -m pip install "mcp<2"
```

### Port 8000 already in use

Windows:

```powershell
netstat -ano | findstr :8000
```

Terminate the process if required.

### Cloudflare Tunnel not working

Restart:

```powershell
cloudflared tunnel --url http://127.0.0.1:8000
```

Then update the Agora MCP URL with the new tunnel URL.

### MCP returns 404

Verify that the configured endpoint is:

```text
/mcp
```

For example:

```text
https://your-domain.trycloudflare.com/mcp
```

and not only:

```text
https://your-domain.trycloudflare.com/
```

## Current Status

| Component | Status |
|---|---|
| Agora Voice Agent | 🟡 Development |
| Rahul Sales Agent | 🟡 Development |
| MCP Server | 🟡 Development |
| FastMCP | ✅ |
| Google Sheets | ✅ |
| Google Apps Script | ✅ |
| Student Lookup | ✅ |
| Call Outcome Update | ✅ |
| WhatsApp Integration | 🟡 |
| Cloudflare Tunnel | ✅ |
| Agora MCP Connection | 🟡 |
| Production Authentication | ⏳ |

## Future Enhancements

### CRM Integration

The MCP layer can be extended to support:

```text
                    MCP
                     │
       ┌─────────────┼─────────────┐
       ▼             ▼             ▼
   Google Sheets     CRM       WhatsApp
       │             │             │
       └─────────────┼─────────────┘
                     │
                  Calendar
```

### Automated Follow-up

```text
Call
 │
 ▼
Lead Qualification
 │
 ▼
CRM Update
 │
 ├── WhatsApp
 │
 ├── Email
 │
 └── Calendar Booking
       │
       ▼
   Sales Follow-up
```

### Analytics

Future analytics can include:

- Total calls
- Qualified leads
- Hot leads
- Conversion rate
- Follow-up rate
- Course-wise leads
- Call duration
- Objection analysis
- Agent performance
- Student response rate

## Project Vision

Rahul-ZelixAI Sales Agent demonstrates how AI voice agents can interact with real business systems using MCP.

Instead of building one large monolithic AI system, MCP provides a controlled tool layer:

```text
                 ┌──────────────────┐
                 │    AI Agent      │
                 │      Rahul       │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │   MCP Tool Layer │
                 └────────┬─────────┘
                          │
             ┌────────────┼────────────┐
             ▼            ▼            ▼
          Sheets         CRM       WhatsApp
```

This architecture makes the agent easier to extend, maintain, secure, and integrate with enterprise workflows.

## Author

**Arpit Dhote**

AI / Data Science | Generative AI | Agentic AI | MCP

Built for **ZelixAI**.

## License

Add the appropriate license for the project.

Example:

```text
MIT License
```
