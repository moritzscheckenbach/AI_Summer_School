import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

from icalendar import Calendar, Event
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent


def schedule_an_appointment(description: str, date: datetime, duration: float, location: str) -> str:
    """Schedule an appointment in the user's calendar.

    Args:
        date (utc): The date and time of the appointment e.g. 2025-09-24 15:00:00.
        description: A brief description of the appointment.

    Returns:
        A confirmation message indicating the appointment has been scheduled.
    """
    print(f"Calendar tool called")
    # Create calendar
    cal = Calendar()
    cal.add("prodid", "-//AI Calendar//mxm.dk//")
    cal.add("version", "2.0")

    # Create event
    event = Event()
    event.add("summary", description)
    event.add("dtstart", date.replace(tzinfo=timezone.utc))
    event.add("dtend", date.replace(tzinfo=timezone.utc) + timedelta(hours=duration))
    event.add("dtstamp", datetime.now(tz=timezone.utc))
    if location:
        event.add("location", location)

    # Add event to calendar
    cal.add_component(event)

    # Write to file
    calendar_path = Path(f"{description.replace(' ', '_')}.ics")
    with open(calendar_path, "wb") as f:
        f.write(cal.to_ical())
    print(f"Calendar tool finished")
    return f"Appointment scheduled: '{description}' on {date.strftime('%Y-%m-%d %H:%M')}. ICS file created: {calendar_path.resolve()}"


def test_schedule_an_appointment() -> None:
    """Test the schedule_an_appointment tool."""
    description = "Meeting with AI team"
    date = datetime(2025, 9, 24, 15, 0)
    print(date)
    duration = 1.0
    location = "Conference Room A"

    result = schedule_an_appointment(description, date, duration, location)
    assert "Appointment scheduled" in result
    assert f"{description.replace(' ', '_')}.ics" in result


def search_engine_tool(query: str) -> str:
    # Tool
    search_tool = TavilySearch(max_results=3)

    # Model
    llm = ChatOpenAI(
        model="openai/gpt-oss-120b:free",  # openai/gpt-4o-mini
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1",
        temperature=0,
    )
    # Optional: peristent Memory
    memory = MemorySaver()
    agent = create_react_agent(llm, tools=[search_tool], checkpointer=memory)

    state = {"messages": [HumanMessage(content=query)]}

    config = {"configurable": {"thread_id": "ai-news-thread-001"}}

    result = agent.invoke(state, config=config)

    last_msg = result["messages"][-1]
    try:
        last_msg.pretty_print()
    except Exception:
        print(getattr(last_msg, "content", last_msg))


def test_search_engine_tool() -> None:
    query = "What are the latest advancements in AI for 2024?"
    search_engine_tool(query)


if __name__ == "__main__":
    # test_schedule_an_appointment()
    test_search_engine_tool()
