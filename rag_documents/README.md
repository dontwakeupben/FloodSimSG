# RAG Document Generation Prompt

Use this prompt with an AI (ChatGPT, Claude, Azure OpenAI) to generate comprehensive Singapore flood-related documents for the chatbot.

---

## AI Prompt for Document Generation

```
You are a technical documentation specialist creating educational content about Singapore flood safety and management. Generate comprehensive, factual documents that will be used in an AI-powered flood safety chatbot for a game simulation.

CONTEXT:
The game simulates three locations in Singapore:
- ION Orchard (High ground, 18m elevation, underground MRT access)
- Orchard Road (Street level, flash flood prone)
- Tanglin Carpark (Basement, dangerous, flooded in 2010/2011)

GENERATE THE FOLLOWING DOCUMENTS:

1. PUB_FLOOD_MANAGEMENT_GUIDELINES.txt
   - PUB's official flood management protocols
   - Drainage infrastructure information
   - How Singapore prevents floods
   - Maintenance schedules and systems

2. SINGAPORE_PUBLIC_TRANSPORT_FLOOD_ADVISORIES.txt
   - MRT operations during floods
   - Bus route disruptions
   - Alternative transport options
   - Station closures and announcements
   - SMRT/SBS Transit protocols

3. FLOOD_RISK_BY_AREA.txt
   - Flood-prone areas in Singapore
   - Historical flood locations
   - Elevation data and flood thresholds
   - Risk assessment methodology

4. TANGLIN_2010_2011_FLOOD_INCIDENTS.txt
   - Detailed timeline of the floods
   - Damage assessment
   - Response and recovery
   - Lessons learned and improvements

5. ORCHARD_ROAD_FLOOD_HISTORY.txt
   - Historical flooding events on Orchard Road
   - Causes (construction, drainage, etc.)
   - Road closures and diversions
   - Shopping mall impacts

6. EMERGENCY_RESPONSE_PROCEDURES.txt
   - SCDF flood response protocols
   - Evacuation procedures
   - Emergency shelters
   - Communication during disasters

7. SINGAPORE_WEATHER_PATTERNS.txt
   - Monsoon seasons
   - Rainfall intensity classifications
   - Weather forecasting
   - NEA weather warnings

8. FLOOD_SAFETY_FOR_DRIVERS.txt
   - What to do if car stalls in flood
   - Insurance claims for flood damage
   - Vehicle preparation
   - Alternative parking during warnings

9. FLOOD_SAFETY_FOR_PEDESTRIANS.txt
   - Walking during heavy rain
   - Avoiding underground crossings
   - Safe routes during floods
   - Footwear and clothing advice

10. PROPERTY_PROTECTION_GUIDE.txt
    - Protecting homes from floods
    - Sandbag deployment
    - Electrical safety
    - Insurance coverage

FORMAT REQUIREMENTS:
- Plain text format (.txt files)
- Use clear section headers with dashes/equals
- Include specific facts, dates, and statistics where possible
- Keep paragraphs concise (3-5 sentences)
- Use bullet points for lists
- Include emergency contact numbers
- Add historical context and real examples
- Mention specific Singapore locations and agencies (PUB, SCDF, NEA, SMRT, SBS)
- Tone: Informative, authoritative, educational

Each document should be 500-1000 words and cover the topic comprehensively but accessibly for general public education.
```

---

## Alternative: Single Mega-Prompt

If you want the AI to generate ALL documents in one go:

```
Generate 10 separate flood safety documents for Singapore as plain text files. Each should be 500-800 words, well-structured with headers, and include specific Singapore agencies, locations, and emergency contacts.

FILE 1: PUB_FLOOD_MANAGEMENT_GUIDELINES.txt
[Content about drainage systems, flood prevention]

FILE 2: SINGAPORE_PUBLIC_TRANSPORT_FLOOD_ADVISORIES.txt  
[Content about MRT/bus during floods]

FILE 3: FLOOD_RISK_BY_AREA.txt
[Content about flood-prone zones]

FILE 4: TANGLIN_2010_2011_FLOOD_INCIDENTS.txt
[Detailed incident report]

FILE 5: ORCHARD_ROAD_FLOOD_HISTORY.txt
[Historical flooding events]

FILE 6: EMERGENCY_RESPONSE_PROCEDURES.txt
[SCDF protocols, evacuation]

FILE 7: SINGAPORE_WEATHER_PATTERNS.txt
[Monsoon, rainfall, NEA warnings]

FILE 8: FLOOD_SAFETY_FOR_DRIVERS.txt
[Vehicle safety, insurance]

FILE 9: FLOOD_SAFETY_FOR_PEDESTRIANS.txt
[Walking safety, routes]

FILE 10: PROPERTY_PROTECTION_GUIDE.txt
[Home protection, sandbags]

Format each with clear headers (=== Section Name ===) and include specific contact numbers (999, 995, 1800-CALL-PUB, etc.).
```

---

## Tips for Best Results

1. **Use GPT-4 or Claude** for most accurate Singapore-specific information
2. **Fact-check** generated content against official PUB/SCDF/NEA websites
3. **Add your own knowledge** about local flood experiences
4. **Include recent events** (e.g., 2023 flash floods at Orchard Road)
5. **Keep updating** as new flood management systems are implemented

---

## Sample Document Structure

```
TITLE: Topic Name

=== Overview ===
Brief introduction to the topic

=== Key Information ===
- Bullet point 1
- Bullet point 2
- Bullet point 3

=== Procedures ===
Step-by-step instructions

=== Emergency Contacts ===
- Police/Fire: 999
- SCDF: 995
- PUB: 1800-CALL-PUB

=== Historical Context ===
Relevant past events

=== References ===
Mention source agencies (optional)
```
