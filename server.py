import os
import requests
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

GOOGLE_SCRIPT_URL = os.getenv("GOOGLE_SCRIPT_URL")

WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")

mcp = FastMCP("Student Followup MCP")


# --------------------------------------------------
# GOOGLE SHEETS
# --------------------------------------------------

@mcp.tool()
def get_student(phone: str) -> dict:
    """
    Find a student in the Google Sheet using their phone number.

    Args:
        phone: Student phone number including country code.
    """

    if not GOOGLE_SCRIPT_URL:
        return {
            "success": False,
            "error": "GOOGLE_SCRIPT_URL is not configured"
        }

    phone = (
        phone
        .replace("+", "")
        .replace(" ", "")
        .replace("-", "")
    )

    try:

        response = requests.get(
            GOOGLE_SCRIPT_URL,
            params={
                "action": "get_student",
                "phone": phone
            },
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        return data

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }


# --------------------------------------------------
# UPDATE CALL STATUS
# --------------------------------------------------

@mcp.tool()
def complete_call(
    phone: str,
    outcome: str
) -> dict:
    """
    Mark the student's call as completed and store the call outcome.

    Args:
        phone: Student phone number.
        outcome: Short summary of the call outcome.
    """

    if not GOOGLE_SCRIPT_URL:
        return {
            "success": False,
            "error": "GOOGLE_SCRIPT_URL is not configured"
        }

    phone = (
        phone
        .replace("+", "")
        .replace(" ", "")
        .replace("-", "")
    )

    try:

        response = requests.post(
            GOOGLE_SCRIPT_URL,
            json={
                "action": "complete_call",
                "phone": phone,
                "outcome": outcome
            },
            timeout=10
        )

        response.raise_for_status()

        return response.json()

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }


# --------------------------------------------------
# WHATSAPP
# --------------------------------------------------

@mcp.tool()
def send_whatsapp(phone: str, name: str, course: str):

    message = (
        f"Hi {name}, thank you for speaking with us today! "
        f"As discussed, here are the details regarding "
        f"our {course} program."
    )

    print("WHATSAPP MESSAGE")
    print("To:", phone)
    print(message)

    return {
        "success": True,
        "phone": phone,
        "message": message,
        "status": "MOCK_SENT"
    }

# --------------------------------------------------
# COMPLETE FOLLOW-UP
# --------------------------------------------------

@mcp.tool()
def complete_student_followup(
    phone: str,
    outcome: str
) -> dict:
    """
    Complete the entire post-call workflow.

    1. Find the student.
    2. Update the call status.
    3. Send WhatsApp follow-up.
    """

    # ----------------------------------------------
    # STEP 1: Find student
    # ----------------------------------------------

    student_result = get_student(phone)

    if not student_result.get("found", False):

        return {
            "success": False,
            "step": "get_student",
            "error": "Student not found",
            "student_result": student_result
        }

    name = student_result.get("name")
    course = student_result.get("course")

    # ----------------------------------------------
    # STEP 2: Update call
    # ----------------------------------------------

    call_result = complete_call(
        phone=phone,
        outcome=outcome
    )

    if not call_result.get("success", False):

        return {
            "success": False,
            "step": "complete_call",
            "student": name,
            "error": call_result
        }

    # ----------------------------------------------
    # STEP 3: WhatsApp
    # ----------------------------------------------

    whatsapp_result = send_whatsapp(
        phone=phone,
        name=name,
        course=course
    )

    return {
        "success": whatsapp_result.get("success", False),
        "student": name,
        "course": course,
        "call_update": call_result,
        "whatsapp": whatsapp_result
    }


# --------------------------------------------------
# START MCP SERVER
# --------------------------------------------------



if __name__ == "__main__":
    mcp.run(transport="sse")