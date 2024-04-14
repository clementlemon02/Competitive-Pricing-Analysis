from Backend.pricesimulation.agent import PassengerAgent

def test_passenger_agent_creation():
    agent = PassengerAgent(1, None, "Adult")
    assert agent is not None

def test_passenger_agent_demographic():
    agent = PassengerAgent(1, None, "Adult")
    assert agent.demographic == "Adult"
    
def test_passenger_agent_preferences():
    agent_adult = PassengerAgent(1, None, "Adult")
    agent_senior = PassengerAgent(2, None, "Senior")
    agent_student = PassengerAgent(3, None, "Student")

    assert "accessibility" in agent_adult.preferences
    assert "leisure_time" in agent_adult.preferences

def test_passenger_agent_willingness_to_pay():
    agent_adult = PassengerAgent(1, None, "Adult")
    agent_senior = PassengerAgent(2, None, "Senior")
    agent_student = PassengerAgent(3, None, "Student")

    assert "base_price" in agent_adult.willingness_to_pay
    assert "max_price" in agent_adult.willingness_to_pay
    assert "price_sensitivity" in agent_adult.willingness_to_pay

def test_passenger_agent_value_perception():
    agent_adult = PassengerAgent(1, None, "Adult")
    agent_senior = PassengerAgent(2, None, "Senior")
    agent_student = PassengerAgent(3, None, "Student")

    assert "expected_satisfaction" in agent_adult.value_perception
    assert "word_of_mouth" in agent_adult.value_perception

def test_passenger_agent_ticket_purchase_status():
    agent = PassengerAgent(1, None, "Adult")
    assert agent.ticket_purchased is False



