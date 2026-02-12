# generate_flood_docs.py
# Run this script to create all 10 FloodSimSG RAG documents

files_content = {
    "PUB_FLOOD_MANAGEMENT_GUIDELINES.txt": """PUB FLOOD MANAGEMENT GUIDELINES
Singapore's National Water Agency

=== Overview ===
PUB (Public Utilities Board) is Singapore's national water agency responsible for managing the country's water supply, drainage, and sewerage systems. Since 2001, PUB has been the lead agency for flood management, implementing a comprehensive, multi-pronged approach to minimize flood risks in the tropical, urbanized environment of Singapore.

=== Drainage Infrastructure ===
Singapore's drainage system comprises over 8,000 kilometers of drains and canals, including major waterways like the Singapore River, Kallang River, and Rochor Canal. The system is designed to handle intense rainfall typical of tropical thunderstorms, with drains sized to accommodate runoff from upstream catchments.

Key infrastructure includes:
- 32 major rivers and canals
- Over 5,000km of public drains
- 17 reservoir schemes integrated with flood control
- Underground stormwater storage tanks (e.g., Stamford Detention Tank)
- Smart drainage systems with real-time monitoring

=== Flood Prevention Strategy ===
PUB employs a "Source-Pathway-Receptor" approach:
- Source: Minimize runoff through porous pavement, green roofs, and rainwater harvesting
- Pathway: Ensure drains and canals have adequate capacity and are free from obstructions
- Receptor: Protect properties through platform levels, flood barriers, and public education

The Code of Practice on Surface Water Drainage mandates that all developments provide on-site detention tanks to slow down stormwater discharge into public drains, reducing peak flows during heavy rain.

=== Maintenance Schedules ===
PUB conducts rigorous maintenance year-round:
- Daily inspection of flood-prone areas during monsoon seasons
- Weekly cleaning of critical drains and trash traps
- Quarterly desilting of major canals
- Annual comprehensive drainage system audits
- Pre-monsoon inspections (March and September)

The Quick Response Teams (QRTs) are activated during heavy rain to monitor hotspots and clear blockages within 30 minutes of detection.

=== Monitoring and Technology ===
PUB operates a comprehensive flood monitoring network:
- 250+ water level sensors across Singapore
- 130+ CCTVs monitoring critical drainage points
- Real-time data transmission to PUB Operations Centre
- MyWaters mobile app for public flood alerts
- Integration with NEA's weather radar systems

=== Contact Information ===
- 24-hour Flood Duty Officer: 1800-CALL-PUB (1800-2255-782)
- Emergency (Police/Fire): 999
- SCDF: 995
- PUB Website: www.pub.gov.sg""",

    "SINGAPORE_PUBLIC_TRANSPORT_FLOOD_ADVISORIES.txt": """SINGAPORE PUBLIC TRANSPORT FLOOD ADVISORIES
MRT and Bus Operations During Flooding Events

=== MRT Flood Resilience ===
Singapore's Mass Rapid Transit (MRT) system is designed with multiple flood protection measures due to its extensive underground network. Station entrances are elevated minimum 1.2m above ground level, with additional flood barriers (demountable or automatic) deployed during heavy rain warnings.

Critical flood prevention infrastructure includes:
- Raised station entrances and ventilation shafts
- Automatic flood barrier systems at 23 vulnerable stations
- Water-tight doors and seals for underground facilities
- 24/7 Operations Control Centre monitoring weather alerts
- Portable flood barriers stored at all underground stations

=== Station Closure Protocols ===
When water levels threaten station safety:
1. Alert Stage: Water detected near entrance - monitoring intensified
2. Warning Stage: Water approaching critical level - barriers deployed
3. Closure Stage: Water entering station - immediate evacuation and closure

Recent closures due to flooding:
- 2023: Bencoolen Station (flash flood at entrance)
- 2021: Clarke Quay area stations (preventive measures)
- 2010: Orchard Station (Tanglin flooding impact)

=== Bus Operations During Floods ===
Bus services are the most affected during flash floods. SBS Transit and SMRT Bus coordinate closely with LTA and PUB:

Bus Disruption Procedures:
- Real-time diversion based on PUB flood alerts
- Bus Captain authority to divert when safety is compromised
- Alternative routes pre-planned for 50+ flood-prone road segments
- Service updates via Bus Stop displays, apps, and social media

High-risk bus routes:
- Services using Orchard Road, Bukit Timah Road, and Thomson Road
- Routes passing through low-lying areas like Bukit Panjang, Admiralty
- Industrial estate services in Pioneer and Tuas (ponding prone)

=== Alternative Transport Options ===
When primary modes fail:
- Free bridging bus services between affected MRT stations
- Activated within 15 minutes of service disruption
- Pickup points clearly marked at alternative stations
- Integration with Grab, Gojek, and TADA for surge monitoring

=== Communication Protocols ===
Public notification hierarchy:
1. MyTransport.sg app push notifications
2. Station announcements (English, Mandarin, Malay, Tamil)
3. Social media (Twitter/X @SBSTransit and @SMRT_Singapore)
4. News radio (93.8FM, 95.8FM, 89.7FM)
5. Electronic signboards at bus stops and stations

=== Safety Guidelines for Commuters ===
During heavy rain/flood warnings:
- Avoid underground passages if water is visible at entrances
- Do not attempt to wade through flooded bus stops (risk of open manholes)
- Check PUB's MyWaters app before traveling
- Allow extra 30-45 minutes for journeys during monsoon periods
- Follow staff instructions; do not force open train doors

=== Emergency Contacts ===
- MRT Emergency: Press emergency button in trains/stations
- SMRT Hotline: 1800-336-8900
- SBS Transit: 1800-287-2727
- LTA OneMotoring: 1800-2255-582
- PUB Flood Alert: 1800-CALL-PUB""",

    "FLOOD_RISK_BY_AREA.txt": """FLOOD RISK BY AREA
Singapore Flood-Prone Locations and Risk Assessment

=== Methodology ===
PUB classifies flood risk using a combination of:
- Historical flood incidence data (post-2000)
- Terrain elevation analysis (LiDAR mapping)
- Drainage capacity modeling
- Land use changes and urban development
- Climate change projections (increasing rainfall intensity)

Risk categories:
- High Risk: Flooded multiple times in past decade, significant property damage potential
- Medium Risk: Occasional flash floods, mainly road-level inundation
- Low Risk: Rare flooding, quick dissipation, minor inconvenience

=== High-Risk Zones ===

Orchard Road Area:
- Tanglin Mall/Tanglin Carpark (Basement level, flooded 2010/2011)
- Orchard Road intersections with Scotts Road/Paterson Road
- Liat Towers basement (flooded 2010)
- Far East Shopping Centre vicinity
Risk factors: Low-lying topography, intense commercial development, limited drainage capacity in older sections

Bukit Timah Area:
- Bukit Timah Road (between Sixth Avenue and Woodcut Road)
- Clementi Road near Ngee Ann Polytechnic
- Dunearn Road underpasses
Risk factors: Natural valley topography, upstream catchment from Central Catchment Nature Reserve

Northern Areas:
- Admiralty Road West (industrial estates)
- Woodlands Avenue 12
- Yishun Avenue 5/Ring Road
Risk factors: Older drainage infrastructure, industrial runoff, flat terrain

Eastern Industrial:
- Paya Lebar Road/Airport Road
- Tampines Avenue 10 industrial area
- Changi Business Park (low-lying sections)
Risk factors: High runoff from concrete surfaces, tidal influences

=== Medium-Risk Zones ===

Central Business District:
- Robinson Road (occasional flash floods)
- Shenton Way basements
- Cecil Street
Risk factors: Dense development, but modern drainage infrastructure

Western Regions:
- Jurong West Avenue 1
- Pioneer Road junctions
- Tuas industrial areas (increasing risk with development)
Risk factors: Reclaimed land, ongoing construction, sediment runoff

=== Game-Specific Locations Profile ===

ION Orchard (Low Risk):
- Elevation: 18m above sea level
- Flood risk: Minimal due to high elevation
- Vulnerability: Underground MRT connection (ION Station) subject to standard MRT protocols
- Historical data: No flooding incidents since opening in 2009

Orchard Road (High Risk):
- Elevation: 10-12m varying along stretch
- Flood risk: Flash flooding during intense thunderstorms (>50mm/hour)
- Vulnerable points: Intersections, basement carparks, underground pedestrian crossings
- Historical data: Major floods 2010, 2011, 2017, 2023

Tanglin Carpark (Critical Risk):
- Elevation: 8m (basement level effectively 3-4m below road)
- Flood risk: Severe basement flooding within 30 minutes of heavy rain
- Historical data: Completely submerged December 2010 and January 2011
- Current status: Improved drainage pumps installed, but remains high-risk

=== Warning Thresholds ===
PUB issues flood warnings when:
- Water level reaches 90% of drain capacity
- Rainfall exceeds 50mm/hour in high-risk zones
- Tide levels coincide with heavy rain (compound flooding risk)

=== Real-Time Monitoring ===
Access current flood status:
- PUB MyWaters app (iOS/Android)
- Public Utilities Board website flood map
- LTA OneMotoring road closure updates
- Radio broadcast during severe weather""",

    "TANGLIN_2010_2011_FLOOD_INCIDENTS.txt": """TANGLIN 2010-2011 FLOOD INCIDENTS
Case Study of Singapore's Worst Recent Urban Flooding

=== December 23, 2010 Incident ===

Timeline:
- 10:30 AM: Heavy rain begins over central Singapore
- 11:15 AM: Rainfall intensity peaks at 100.6mm/hour (highest in 30 years for the area)
- 11:30 AM: Water overflows from Stamford Canal
- 11:45 AM: Tanglin Mall basement carpark begins flooding
- 12:00 PM: Liat Towers basement completely submerged (3m depth)
- 12:15 PM: Tanglin Carpark reaches full inundation (50+ vehicles submerged)
- 1:00 PM: Rain subsides, pumping operations begin
- 6:00 PM: Water levels recede sufficiently for damage assessment

Immediate Impact:
- Tanglin Mall: 150 vehicles damaged/destroyed in B2 and B3 carpark levels
- Liat Towers: 30+ luxury vehicles destroyed, ground floor shops flooded
- Orchard Road: Traffic paralysis for 6 hours
- Estimated damage: $5-7 million (vehicles and property)

=== January 30, 2011 Incident ===

Timeline:
- 2:15 PM: Intense thunderstorm develops
- 2:45 PM: Rainfall reaches 80mm/hour
- 3:00 PM: Tanglin Carpark floods again (repeat incident)
- 3:15 PM: Water enters Tanglin Mall basement retail level
- 3:30 PM: Scotts Road/Orchard Road intersection impassable
- 4:00 PM: MRT station preventive closure (Orchard Station)

Impact:
- Tanglin Mall: Second flooding in 5 weeks, 80+ additional vehicles affected
- Public confidence: Sharp decline in basement parking usage in area
- Insurance claims: Surge in comprehensive auto claims, industry losses >$10 million total

=== Root Cause Analysis ===
Technical Factors:
- Stamford Canal capacity exceeded (designed for 50-year storm, exceeded by 100-year equivalent)
- Rapid development upstream (Ion Orchard construction) increased runoff velocity
- Aging trash trap at canal intake clogged with debris
- Basement carparks below canal overflow level (design flaw)

Operational Factors:
- Warning system insufficient lead time (15 minutes vs. 30 needed for evacuation)
- No automated barriers at carpark entrances
- Insufficient coordination between PUB and mall management
- Public complacency despite earlier warnings

=== Response and Recovery ===

Immediate Actions (2011):
- Installation of temporary flood barriers at Tanglin Mall
- Enhanced pumping capacity (mobile pumps stationed during monsoon)
- 24/7 monitoring of Stamford Canal water levels
- Road closure protocols for Orchard Road when canal reaches 80% capacity

Long-term Improvements (2011-2015):
- Stamford Detention Tank constructed (2014) - 15 million liter capacity underground storage
- Canal widening and deepening along Tanglin Road stretch
- Mandatory flood barriers for all new basement developments in zone
- Improved trash traps with automated monitoring

Compensation and Support:
- PUB ex-gratia payments for uninsured vehicle losses (partial coverage)
- Business interruption support for affected retailers
- Free vehicle towing and assessment services
- Public apology from Minister for Environment and Water Resources

=== Lessons Learned ===

Engineering Standards:
- Basement carparks now required to be 1.2m above 100-year flood levels OR have approved flood mitigation systems
- All new developments in flood zones must conduct flood impact assessments
- Improved integration of blue-green infrastructure

Public Communication:
- MyWaters app launched (2011) providing real-time flood alerts
- Standardized flood risk signage at carpark entrances
- Regular flood drills in commercial districts
- Enhanced public education on "Don't drive into flooded areas"

System Resilience:
- Redundant pumping systems installed
- Faster deployment of mobile flood barriers (target: 10 minutes)
- Improved weather radar integration (nowcasting accuracy to 15 minutes)
- Coordination protocols between PUB, SCDF, and mall security

=== Current Status (2024) ===
Tanglin area has not experienced major flooding since 2011 infrastructure upgrades. However, Tanglin Carpark remains a high-risk location in PUB's database, with permanent flood barriers installed and automatic pump systems. The area serves as the primary case study for Singapore's flood resilience improvements.""",

    "ORCHARD_ROAD_FLOOD_HISTORY.txt": """ORCHARD ROAD FLOOD HISTORY
Flash Flooding in Singapore's Premier Shopping District

=== Historical Context ===
Orchard Road, despite being Singapore's premier shopping and tourism belt, has a documented history of flooding dating back to the 1950s. The area's topography (gentle valley between Bukit Timah and Fort Canning) combined with intense urban development creates natural runoff challenges.

Pre-2000 Incidents:
- 1954, 1969, 1978: Minor flooding during exceptionally wet monsoons
- 1980s-1990s: Increasing frequency due to development pressure
- All incidents pre-2000 were primarily road-level inundation lasting 1-2 hours

=== Modern Era Major Floods ===

June 16, 2010:
- Location: Orchard Road/Scotts Road junction, Paterson Road
- Cause: 70mm rainfall in 2 hours, construction debris blocking drains
- Impact: Traffic disruption for 4 hours, water up to 0.5m on road
- Response: Temporary drainage improvements, construction site audits

December 23, 2010 (Major Event):
- See detailed timeline in Tanglin 2010-2011 document
- Most severe flooding in Singapore's modern history
- Catalyzed major infrastructure investment

January 30, 2011:
- Repeat flooding at Tanglin Mall/Liat Towers
- Proved that December 2010 was not an isolated incident
- Led to resignation of PUB chairman and organizational restructuring

December 8, 2017:
- Location: Orchard Road near Tanglin Mall (same area as 2010/2011)
- Cause: 75mm rainfall in 1.5 hours, high tide coinciding with rain
- Impact: Road closure for 3 hours, water entered Tanglin Mall basement (prevented full flooding by new barriers)
- Significance: Test of new infrastructure - barriers and pumps functioned correctly, damage minimized

August 20, 2021:
- Location: Orchard Boulevard/Grange Road
- Cause: Intense localized thunderstorm, 85mm/hour rainfall
- Impact: Road flooding 0.3m depth, minor basement seepage at ION Orchard (parking B4)
- Response: Rapid clearance within 90 minutes, no vehicle damage

April 17, 2023:
- Location: Orchard Road (between Scotts Road and Bideford Road)
- Cause: 50mm rainfall in 45 minutes, drain maintenance backlog post-COVID
- Impact: 2-hour road closure, water entered Wheelock Place basement (retail level)
- Response: Enhanced maintenance schedules reinstated

=== Contributing Factors ===

Urban Development Pressures:
- Continuous construction (ION Orchard 2009, Somerset MRT upgrades, new developments)
- Reduced permeable surfaces increasing runoff by 40% since 2000
- Basement excavation altering groundwater flows

Drainage Challenges:
- Stamford Canal (main drainage artery) constrained by urban infrastructure
- Aging pipes (1960s-70s installation) in some sections
- Competition for underground space (MRT, utilities, fiber optics)

Climate Factors:
- Increasing rainfall intensity (15% increase in maximum hourly rainfall since 1980)
- Urban heat island effect intensifying localized thunderstorms
- Sea level rise reducing tidal discharge efficiency (1.5mm/year rise)

=== Road Closure Protocols ===

Automatic Closure Triggers:
- Water depth >0.15m on road surface
- Visibility <50m due to rain/spray
- Debris or tree fall blocking lanes
- Police/PUB officer discretion for safety

Closure Procedures:
1. Police Traffic Police deploy barriers at key junctions
2. Electronic signboards activated ("ROAD CLOSED - FLOODING")
3. LTA OneMotoring system updated
4. GPS navigation services (Google Maps, Waze) notified
5. Public transport alerts issued

Alternative Routes:
- Via Napier Road and Clemenceau Avenue (western detour)
- Via Bras Basah Road and River Valley Road (eastern detour)
- Via Bukit Timah Road and Dunearn Road (northern detour)

=== Shopping Mall Impacts ===

Affected Properties (Historical):
- Tanglin Mall (2010, 2011, 2017)
- Liat Towers (2010, 2011)
- Wheelock Place (2017, 2023)
- ION Orchard (minor seepage 2021)
- Ngee Ann City (minor incidents 2010, 2016)

Mitigation Measures Implemented:
- Automatic flood barriers (Tanglin Mall, Liat Towers)
- Enhanced pumping capacity (all major malls)
- Raised entrance levels (newer developments)
- 24/7 security monitoring during heavy rain
- Tenant education and evacuation drills

Business Continuity:
- Most malls now carry flood insurance
- 4-hour business interruption protocols
- Tenant support funds (major mall operators)
- Alternative parking arrangements with nearby buildings

=== Current Resilience Status ===

As of 2024:
- Orchard Road flood frequency reduced by 80% since 2011 infrastructure upgrades
- Average water clearance time improved from 4 hours to 90 minutes
- No major vehicle damage incidents since 2011 (thanks to barriers and warnings)
- Remaining risk: Extreme weather events (>100mm/hour) exceeding 200-year design standards

Ongoing Projects:
- Deep Tunnel Sewerage System Phase 2 (additional flood storage)
- Smart sensors every 100m along Orchard Road
- Green infrastructure integration (porous pavement trials)
- Underground flood bypass tunnels (planning phase)

=== Tourist and Visitor Guidance ===

During Heavy Rain:
- Seek shelter in major malls (ION, Ngee Ann City, Paragon) - all have flood protection
- Avoid basement levels if rain exceeds 30 minutes continuously
- Use Orchard MRT underground walkway network (elevated above flood risk)
- Check mall websites for closure announcements

Emergency Contacts:
- Orchard Road Business Association: 6737-3855
- PUB 24-hour: 1800-CALL-PUB
- Police: 999""",

    "EMERGENCY_RESPONSE_PROCEDURES.txt": """EMERGENCY RESPONSE PROCEDURES
SCDF and Agency Coordination During Flood Events

=== Command Structure ===

National Level:
- Ministry of Home Affairs (MHA) provides overall coordination
- SCDF (Singapore Civil Defence Force) leads ground response
- PUB manages drainage and technical flood mitigation
- NEA monitors weather and issues warnings
- LTA manages road closures and transport

Local Level:
- Police Coast Guard (for coastal flooding)
- Divisional Disaster Management Teams (DMT)
- Community Emergency Response Teams (CERT)
- Town Council maintenance crews

=== SCDF Flood Response Protocols ===

Alert Levels:

Level 1 (Monitoring):
- Trigger: Heavy rain forecast or minor ponding
- Action: Standby mode, equipment checks
- Duration: Until all-clear issued

Level 2 (Activation):
- Trigger: Flash flood warning from PUB or water levels rising
- Action: Deployment of 2-3 fire appliances to affected areas
- Equipment: Portable pumps, rescue boats, life jackets
- Response time: 15 minutes to scene

Level 3 (Full Deployment):
- Trigger: Confirmed flooding with property damage or rescue needs
- Action: Battalion-level response, 10+ appliances
- Additional resources: Disaster assistance and rescue team (DART), marine rescue
- Coordination: SCDF Operations Centre activated

=== Evacuation Procedures ===

Residential Evacuation:
1. Warning: Door-to-door alerts by Police and CERT members
2. Assembly: Residents move to designated assembly areas (usually void decks or shelters)
3. Transport: SCDF buses or ambulances for mobility-impaired
4. Shelter: Transfer to official evacuation centers (community centers, schools)

Priority Evacuation Groups:
- Elderly living alone
- Ground-floor residents in flood zones
- Hospital and care facility patients
- Special needs individuals

Commercial Building Evacuation:
- Security leads initial evacuation using PA systems
- Fire wardens check all floors and restrooms
- Elevators prohibited (risk of entrapment if power fails)
- Assembly at designated muster points away from building

Transport Evacuation:
- MRT stations: Staff-guided evacuation via nearest exit, avoid flooded entrances
- Buses: Drivers assess safety, may request passenger evacuation if water reaches wheel level
- Vehicles: Abandon only if water reaches door level; climb to roof if trapped

=== Emergency Shelters ===

Designated Evacuation Centers:
- 50+ Community Centers (CCs) island-wide equipped for 72-hour stays
- Schools with multi-story buildings (typically HDB neighborhood schools)
- Community shelters in new HDB developments

Facilities Provided:
- Sleeping mats and blankets
- Basic meals (catered or halal-ready-to-eat meals)
- Medical aid stations
- Charging stations for phones
- Sanitary facilities

Registration:
- Mandatory check-in for accountability
- Family reunification services
- Special needs registration for continued support

=== Communication During Disasters ===

Public Alert System:
- SMS alerts via SGSecure app and PublicWarningSystem
- Sirens (if widespread disaster) - 30-second tone
- Radio/TV interruption for emergency broadcasts
- Social media updates (SCDF Facebook, PUB Twitter/X)

On-Ground Communication:
- SCDF uses dedicated 4G/5G networks (priority access)
- Satellite phones for backup in widespread outages
- WhatsApp groups for community coordinators
- Police loudhailer patrols in affected neighborhoods

=== Rescue Operations ===

Water Rescue Techniques:
- Reach: Extend pole or rope from safe position
- Throw: Life rings or flotation devices
- Row: Rescue boats for shallow flooding
- Go: Trained swimmers with safety lines for deep water

Vehicle Submersion Protocol:
1. Approach from upstream side
2. Attempt door opening (pressure equalizes as water fills)
3. If doors stuck, break window (center punch or heavy object)
4. Extract occupants headfirst maintaining spinal alignment
5. Provide immediate first aid for hypothermia/water inhalation

Medical Priorities:
- Drowning/near-drowning: CPR if not breathing
- Hypothermia: Warm dry blankets, gradual rewarming
- Trauma from debris: Standard wound management
- Psychological shock: Calm reassurance, family reunification

=== Recovery Operations ===

Immediate (0-24 hours):
- Damage assessment by SCDF and PUB engineers
- Search and clearance of flooded buildings
- Restoration of critical utilities (power, gas)
- Debris clearance from roads and drains

Short-term (1-7 days):
- Continued shelter operations for displaced residents
- Water quality testing (PUB)
- Building safety inspections (BCA)
- Insurance assessment teams

Long-term (1-12 months):
- Infrastructure repairs
- Flood prevention improvements
- Community debriefs and psychological support
- Review of response protocols

=== Volunteer and Community Support ===

CERT (Community Emergency Response Team):
- Trained volunteers in HDB estates
- First aid and basic firefighting capabilities
- Assist in door-to-door warnings and initial evacuation
- Coordinate with SCDF upon arrival

PA (People's Association) Integration:
- Community Centers as coordination hubs
- Volunteer registration and deployment
- Distribution of relief supplies
- Family reunification services

=== Emergency Contact Numbers ===

- Emergency (Fire, Ambulance, Rescue): 995
- Police: 999
- Non-emergency Police: 1800-255-0000
- PUB Flood Duty: 1800-CALL-PUB (1800-2255-782)
- SP Group (Electricity/Gas): 1800-778-8888
- Town Council: (varies by constituency, check HDB notice boards)""",

    "SINGAPORE_WEATHER_PATTERNS.txt": """SINGAPORE WEATHER PATTERNS
Monsoons, Rainfall, and Flood Risk Correlation

=== Climate Overview ===
Singapore experiences a tropical rainforest climate (Köppen classification Af) characterized by high humidity (average 84%), consistent temperatures (25-32°C year-round), and abundant rainfall (annual average 2,340mm). The island's position 137km north of the equator results in minimal seasonal temperature variation but distinct wet and dry phases driven by monsoon wind patterns.

=== Monsoon Seasons ===

Northeast Monsoon (December to March):
- Wet phase: December to January (peak flooding risk)
- Dry phase: February to March
- Wind direction: Northeast, carrying moisture from South China Sea
- Characteristics: Prolonged moderate to heavy rain, lasting 2-3 days
- Monthly rainfall: 250-350mm in December/January
- Flood risk: Moderate but sustained (soil saturation leads to flash floods)

Southwest Monsoon (June to September):
- Generally drier season
- Wind direction: Southeast/Southwest
- Characteristics: Short, intense thunderstorms (afternoon/evening)
- Monthly rainfall: 150-200mm
- Flood risk: High intensity, localized flash floods (urban heat island effect)

Inter-Monsoon Periods (April-May and October-November):
- Most unpredictable weather
- Highest thunderstorm frequency (20-25 days/month)
- Convergence of wind patterns creates atmospheric instability
- "Sumatra Squalls" - organized thunderstorms from west
- Flood risk: Highest for flash floods due to intensity and unpredictability

=== Rainfall Intensity Classifications ===

NEA (National Environment Agency) Classifications:
- Light: <0.5mm/hour
- Moderate: 0.5-4mm/hour
- Heavy: 4-10mm/hour
- Very Heavy: 10-20mm/hour
- Torrential: >20mm/hour

Flood Correlation Thresholds:
- 30mm/hour: Minor ponding in low-lying areas
- 50mm/hour: Flash flood risk in high-risk zones (Orchard, Bukit Timah)
- 70mm/hour: Widespread flash flooding likely, road closures
- 100mm/hour: Major flooding event, emergency response activation

Historical Extremes:
- December 2006: 366mm in 24 hours (Ulu Pandan)
- January 1971: 512mm in 24 hours (highest recorded)
- December 23, 2010: 100.6mm/hour (Tanglin area)
- April 2023: 80mm in 1 hour (western Singapore)

=== Weather Forecasting ===

NEA Capabilities:
- Doppler weather radar (C-band) detecting precipitation 250km radius
- Satellite imagery (Himawari-8) every 10 minutes
- Automated weather stations (80+ across Singapore)
- Nowcasting: 1-2 hour predictions with 80% accuracy
- Short-term: 3-day forecasts updated 4 times daily

Rain Area Information System (RAINS):
- Real-time rainfall intensity maps
- 30-minute rainfall accumulation displays
- Available on NEA website and myENV app
- Updated every 5 minutes during heavy rain

Limitations:
- Tropical convection cells develop rapidly (15-30 minutes)
- Microclimates create localized variations (Orchard vs. Changi can differ significantly)
- Sea breeze interactions difficult to model precisely

=== Warning Systems ===

Heavy Rain Warning (NEA Issues):
- Advisory: Expected rainfall 20-40mm/hour
- Warning: Expected rainfall >40mm/hour
- Dissemination: Radio, TV, SMS via SGSecure, Apps

Flash Flood Alerts (PUB Issues):
- Alert: Water level at 80% drain capacity
- Warning: Water level at 90% capacity or rainfall >50mm/hour sustained
- Critical: Flooding confirmed, avoid area

Haze and Other Considerations:
- While not flood-related, haze (August-October) can complicate emergency responses
- Reduced visibility during heavy rain + haze creates traffic hazards

=== Climate Change Impacts ===

Observed Trends (1980-2024):
- Annual rainfall increased 15% per decade
- Maximum hourly rainfall intensity increased 15%
- Frequency of "extreme" rainfall days (>50mm) doubled
- Consecutive dry days increasing (drought-flood cycles)

Future Projections (2050):
- Average temperature rise 1-3°C
- Rainfall intensity increase 20-30%
- Sea level rise 0.25-0.5m affecting drainage discharge
- More erratic monsoon patterns

Adaptation Measures:
- Drainage infrastructure upgraded to handle 20% more capacity
- "Sponge city" initiatives increasing permeable surfaces
- Real-time monitoring expansion
- Public education on changing risk profiles

=== Seasonal Safety Calendar ===

December-January (High Risk):
- Year-end monsoon peak
- Holiday season with higher traffic volumes
- Tourists unfamiliar with local weather risks
- Precaution: Check weather before basement parking

April-May (Thunderstorm Peak):
- Afternoon storms during school hours
- Flash flood risk during evening commute
- Precaution: Carry umbrella, avoid outdoor activities 3-6pm

June-July (Dry but Intense):
- Short intense storms
- Dry soil leads to rapid runoff
- Precaution: Monitor sudden weather changes

October-November (Second Inter-Monsoon):
- Unpredictable patterns
- Sumatra squalls (early morning)
- Precaution: Morning commuters beware of sudden storms

=== Useful Resources ===

- NEA Weather: www.nea.gov.sg/weather
- myENV app (iOS/Android): Real-time weather and air quality
- PUB MyWaters: Flood monitoring
- Radio: 938NOW, CNA (breaking weather alerts)
- Hotline: 6542-7728 (NEA general enquiries)""",

    "FLOOD_SAFETY_FOR_DRIVERS.txt": """FLOOD SAFETY FOR DRIVERS
Vehicle Protection and Survival During Flooding

=== The Golden Rule ===
Never drive through flooded roads. As little as 15cm (6 inches) of water can cause loss of control in most vehicles, and 30cm (1 foot) can float a car. Floodwater may hide washed-out roads, debris, or open manholes. If you encounter a flooded road, turn around and find an alternative route.

=== Risk Assessment Before Driving ===

Pre-Trip Checks:
- Check PUB MyWaters app for flood alerts
- Check LTA OneMotoring for road closures
- Listen to radio traffic updates (93.8FM, 95.8FM)
- Avoid basement carparks in flood-prone areas during heavy rain warnings

Visual Cues of Danger:
- Water reaching curb level or higher
- Other vehicles stalled in water ahead
- Debris floating on road surface
- Water moving rapidly (even shallow fast water can sweep vehicles away)
- Downed power lines (electrocution risk)

=== If You Must Drive (Heavy Rain) ===

Safe Driving Techniques:
- Reduce speed by 30-50% to prevent hydroplaning
- Maintain 4-second following distance (double normal)
- Use low beam headlights (high beams reflect off rain)
- Avoid sudden braking; pump brakes gently if no ABS
- Stay in middle lanes (roads crown in center, less pooling)

Hazard Zones to Avoid:
- Underpasses and tunnels (flood first, drain last)
- Basements of shopping centers (Tanglin Mall, Liat Towers history)
- Low-lying HDB carparks (ground level)
- Construction zones (sediment and debris block drains)
- Road sections adjacent to canals (overflow points)

=== Vehicle Stalls in Flood - Survival Protocol ===

Immediate Actions (Water Below Door Level):
1. Do not restart engine (hydrolock damage)
2. Turn on hazard lights
3. Call for assistance (tow truck, 1800-2255-582 LTA)
4. Stay in vehicle if water is moving or rising slowly

Emergency Evacuation (Water Rising Above Door Level):
1. Unbuckle seatbelts immediately
2. Unlock all doors (electric locks may fail)
3. Open windows before water reaches halfway (pressure makes opening doors impossible)
4. If windows won't open: Use center punch, heavy object, or headrest metal prongs to break side windows (front/rear windshields are tempered glass, harder to break)
5. Exit through windows, climb to roof
6. Call 995 (SCDF) for rescue
7. Stay on roof until water recedes or rescue arrives - do not attempt to swim

Critical Warnings:
- 15cm of water can knock a person off their feet if moving
- 60cm of water can carry away most SUVs
- Water can hide 3-meter deep drains or sinkholes
- Exhaust pipe submersion can cause carbon monoxide backup into vehicle

=== After the Flood ===

Immediate Vehicle Assessment:
- Do not start the engine if water reached exhaust or intake levels
- Check oil dipstick for water droplets (indicates engine contamination)
- Inspect air filter for water damage
- Check all fluid levels for contamination
- Document damage with photographs for insurance

Professional Inspection Required:
- Electrical systems (ECU, sensors, wiring)
- Brake systems (water contamination reduces effectiveness)
- Transmission and differential fluids
- Interior mold and mildew treatment (health hazard)

Total Loss Indicators:
- Water reached dashboard level (electronics destroyed)
- Saltwater flooding (corrosion inevitable)
- Vehicle submerged >24 hours
- Airbag system compromised

=== Insurance Claims ===

Coverage Types:
- Comprehensive insurance: Covers flood damage (not third-party only)
- "Act of God" coverage: Standard in Singapore comprehensive policies
- Engine damage: Covered if you did not intentionally drive into flood

Claim Process:
1. Report within 24 hours (hotline or app)
2. Do not move vehicle until insurer inspects (unless safety requires)
3. Obtain police report if road flooding caused accident
4. Keep receipts for emergency towing (reimbursable)
5. Hire own assessor if dispute on write-off valuation

Common Exclusions:
- Driving through obvious flood (negligence)
- Starting engine after stalling in water
- Modified vehicles without declared modifications
- Commercial vehicles without appropriate coverage

Fraud Warning:
Intentionally driving into floods to claim insurance constitutes fraud. Insurers share data on "flood magnets" - vehicles repeatedly damaged in floods.

=== Vehicle Preparation ===

Flood-Resistant Measures:
- Know your vehicle's wading depth (check manual, usually 30-50cm for sedans, 50-70cm for SUVs)
- Install snorkel air intake for extreme conditions (off-road vehicles)
- Seal electrical components with dielectric grease
- Park on elevated ground during monsoon warnings

Emergency Kit for Monsoon Season:
- Torchlight and whistle (roof rescue signaling)
- Seatbelt cutter/window hammer (accessible from driver's seat)
- Tow rope and reflective triangles
- Portable phone charger
- Bottle of water and energy bars
- Raincoat (umbrellas useless in high winds)

=== Alternative Parking During Warnings ===

When PUB issues flood warnings for your area:
- Use elevated HDB MSCP (multi-story carpark) levels 3+
- Shopping mall rooftop carparks (ION Orchard, Ngee Ann City)
- Designated high-ground parking (check with Town Council)
- Avoid: Basement carparks in Tanglin, Orchard, Bukit Timah areas

Employer Responsibilities:
- Allow flexible hours during heavy rain warnings
- Provide alternative parking information
- Excuse lateness due to road closures (document with traffic app screenshots)

=== Legal and Safety Responsibilities ===

Motorist duties under Singapore law:
- Section 65, Road Traffic Act: Must not drive without reasonable consideration for others
- Driving through flood splash pedestrians: Fines up to $1,000 and 3 demerit points
- Ignoring road closure signs: $130 fine, possible court prosecution
- Causing wake that damages property: Civil liability

Good Samaritan Protocol:
- Only assist others if safe to do so
- Call 995 for trapped motorists rather than attempting rescue yourself
- Direct traffic around flooded areas if police not yet present
- Document incidents with photos for authorities

=== Emergency Contacts ===
- Vehicle breakdown: Your insurer's 24-hour hotline
- Towing service: AAS 6748-9911 or ComfortDelGro 6552-2222
- LTA TrafficSmart: 1800-2255-582
- SCDF Emergency: 995
- Police: 999""",

    "FLOOD_SAFETY_FOR_PEDESTRIANS.txt": """FLOOD SAFETY FOR PEDESTRIANS
Walking Safety and Route Planning During Floods

=== General Safety Principles ===
Pedestrians are the most vulnerable during flash floods. Unlike vehicles, humans offer no protection from debris, contamination, or electrocution risks. Six inches (15cm) of fast-moving water can knock an adult off their feet, and two feet (60cm) can sweep away even strong swimmers. Singapore's urban floods present unique hazards including open manholes, submerged debris, and contaminated water from drains and sewers.

=== Avoiding Underground Crossings ===

High-Risk Locations:
- Orchard MRT underground passages (connecting ION, Ngee Ann City, Somerset)
- Bras Basah MRT area underground network
- Marina Bay underground city
- HDB estate underground linkways (especially older estates)

Warning Signs to Heed:
- Water visible at entrance steps
- Automatic barriers deployed (indicates management is aware of flood risk)
- Power outages or dimmed emergency lighting
- Unusual odors (sewage backup indication)

Safe Alternatives:
- Use overhead bridges instead of underpasses
- Wait in mall/shops until water recedes (usually 30-60 minutes)
- Surface crossings at traffic lights (higher ground)
- Taxi/Grab instead of walking (split cost with others if stranded)

=== Safe Routes During Floods ===

Route Planning Apps:
- MyWaters (PUB) shows real-time flood locations
- Google Maps indicates road closures (user-reported)
- Avoid "fastest route" during heavy rain; choose "less walking" or bus options

Elevated Routes (Orchard Area Example):
- Instead of Orchard Road level, use ION Sky (outdoor garden, 5th floor)
- Use overhead bridges with covered walkways (connect malls)
- HDB MSCP rooftops as emergency shortcuts (if familiar with area)
- MRT elevated stations as landmarks (Redhill, Tiong Bahru, etc.)

Avoid These Pathways:
- Any path alongside canals (can overflow without warning)
- Covered drains (grates can lift under pressure)
- Construction site perimeters (sediment and equipment hazards)
- Tree-lined paths (lightning and falling branch risks during storms)

=== Footwear and Clothing Advice ===

Appropriate Footwear:
- Water-resistant boots (hunter boots or similar) for known flood areas
- Avoid: Leather shoes (damage), high heels (tripping), flip-flops (slipping, debris cuts)
- Backup shoes: Keep spare dry footwear at office/in bag during monsoon

Clothing Considerations:
- Quick-dry synthetic fabrics (cotton stays wet and cold)
- Bright colors or reflective strips (visibility to drivers in poor conditions)
- Compact umbrella (large golf umbrellas dangerous in winds)
- Waterproof bag or case for electronics and documents

Health Protection:
- Long pants to prevent cuts from hidden debris
- Waterproof bandages for existing wounds (floodwater contamination)
- Insect repellent (mosquitoes breed in stagnant water within 2 days)

=== Walking in Heavy Rain ===

Visibility Measures:
- Wear bright/reflective clothing
- Carry small torchlight (underpasses get dark even during day)
- Use phone flashlight when crossing dim areas (but keep phone protected)

Hazards to Watch For:
- Manhole covers: Can be displaced by water pressure creating sinkholes
- Downed power lines: Stay 10m away, report to 1800-778-8888 (SP Group)
- Open drains: Covers may be removed by water flow or vandals
- Slippery surfaces: Marble mall entrances, metal grates, painted road markings
- Cyclists: They have poor visibility too; give them space

Group Safety:
- Walk in groups of 2+ during severe weather
- Establish meeting points if separated
- Assist elderly or disabled (offer arm, slow pace)
- Children must hold adult hands (water can sweep them away instantly)

=== Specific Location Guidance ===

Orchard Road Precautions:
- Use overhead bridge at ION/Shaun Road (elevated walkway)
- Avoid basement exits (even if shortcut is familiar)
- If caught at Tanglin Mall area, proceed to Hyatt Hotel (high ground, lobby accessible)
- Wait in Wisma Atria or Ngee Ann City (both flood-protected)

HDB Estate Navigation:
- Use covered walkways on upper floors (connecting blocks)
- Void decks may flood; use staircases to cross between blocks
- Avoid open fields (lightning risk, no shelter)
- Community centers act as emergency shelters if stranded

Business District (Raffles Place/Tanjong Pagar):
- Underground network extensive but flood-prone at entry points
- Use elevated sky bridges (OCBC Centre, UOB Plaza connections)
- Marina Bay area: Stick to MRT network or elevated Marina Bay Financial Centre walkways

=== Emergency Procedures ===

If Caught in Rising Water:
1. Move perpendicular to water flow (toward higher ground)
2. Do not attempt to swim against current (exhaustion risk)
3. Grab onto stable objects (railings, trees, fences)
4. Call 995 (SCDF) - they prioritize water rescues
5. Signal rescuers with bright clothing or phone flashlight

If Trapped in Building:
- Move to second floor or higher
- Signal for help from windows (white cloth, flashlight)
- Do not use elevators (power failure risk)
- Listen to battery radio for updates
- Conserve phone battery for emergency calls only

Medical Emergencies:
- Cuts from flood debris: Clean immediately, seek tetanus shot if deep
- Water contact with eyes: Rinse with clean water, seek medical attention (conjunctivitis risk)
- Hypothermia: Remove wet clothing, wrap in blankets even in tropical weather (wind chill effect)
- Respiratory issues: Floodwater aerosols can carry bacteria; use mask if available

=== Hygiene and Health Post-Exposure ===

Immediate Actions:
- Wash hands thoroughly with soap before eating/touching face
- Shower with antiseptic soap as soon as possible
- Wash contaminated clothing separately with hot water
- Disinfect shoes (bleach solution) to prevent mold

Disease Risks from Floodwater:
- Leptospirosis (rat urine): Symptoms 3-10 days later (fever, muscle pain)
- Dengue fever: Mosquitoes breed in stagnant water
- Conjunctivitis: Eye infections from contaminated water
- Skin infections: Cuts exposed to bacteria

When to Seek Medical Attention:
- Fever within 10 days of flood exposure
- Persistent diarrhea or vomiting
- Skin rashes or infected cuts
- Respiratory difficulties

=== Community Support ===

Assisting Neighbors:
- Check on elderly living alone (especially ground floor units)
- Help move valuables to higher shelves if time permits
- Share information about road conditions and shelter locations
- Offer dry clothing and hot drinks to stranded individuals

Reporting Hazards:
- Open manholes/damaged drains: PUB 1800-CALL-PUB
- Fallen trees: NParks 1800-471-7300
- Power lines down: SP Group 1800-778-8888
- General emergencies: 999 (Police) or 995 (SCDF)

=== Emergency Contacts ===
- SCDF (Rescue): 995
- Police: 999
- PUB (Drainage/Flooding): 1800-CALL-PUB
- NEA (Public Health): 1800-2255-632
- SP Group (Electricity): 1800-778-8888""",

    "PROPERTY_PROTECTION_GUIDE.txt": """PROPERTY PROTECTION GUIDE
Home and Business Flood Mitigation Strategies

=== Risk Assessment for Properties ===

Determining Your Risk Level:
- Check PUB's flood map (www.pub.gov.sg/floodmap) by postal code
- Ground floor and basement units highest risk
- Properties built before 1990 may lack modern drainage connections
- Proximity to canals, rivers, or low-lying roads increases risk
- Construction upstream can alter drainage patterns

Flood-Prone Property Types in Singapore:
- Basement carparks (Tanglin Mall model)
- Ground-floor shop houses (Katong, Geylang, Chinatown)
- Bungalows with sunken courtyards or pools
- Industrial units in Pioneer, Tuas (ponding areas)
- Retail units in flood-prone malls (historical Orchard Road properties)

=== Protecting Homes from Floods ===

Structural Modifications:
- Raise electrical outlets and switches minimum 30cm above floor level
- Install backflow prevention valves on toilets and drains (prevents sewage backup)
- Waterproof external walls with sealant (silicone-based for concrete)
- Raise air-conditioning compressor units above potential flood level
- Install sump pumps with battery backup in basements

Entry Point Protection:
- Doorway flood barriers (aluminum or PVC, sandbag alternatives)
- Waterproof seals for garage doors
- Raise entrance thresholds by 15cm where possible
- Install flood skirts around air vents

Landscaping Solutions:
- Create berms (raised earth barriers) around property perimeter
- Install permeable pavers instead of concrete for driveways
- Plant rain gardens to absorb runoff (select flood-tolerant species)
- Ensure downspouts direct water 2m away from foundation

=== Sandbag Deployment ===

Proper Technique:
- Fill sandbags 1/2 to 2/3 full (overfilled bags don't seal well)
- Lay bags like bricks - staggered joints, overlapping seams
- Tamp down each layer to eliminate gaps
- Build pyramid-style walls for stability (wider base than height)
- Place plastic sheeting under sandbag wall for better seal

Strategic Placement:
- Across doorways (inside and outside for double protection)
- Around floor drains (to prevent backup)
- Air conditioning vents (critical for HDB flats)
- Garage entrances (lowest point of most homes)

Alternatives to Traditional Sandbags:
- HydraSacks/HydraSnakes: Gel-filled, expand when wet, lightweight when dry
- Flood gates: Rigid barriers mounted in door frames
- Inflatable dams: Quick deployment for wide openings
- Water-filled tubes: Replace sand, easier to store and deploy

Sources in Singapore:
- PUB provides limited sandbags to flood-prone residents (apply via website)
- Hardware stores: Home-Fix, Selffix, Giant
- Online: Lazada, Shopee (search "flood barriers")
- Construction suppliers for bulk orders

=== Electrical Safety ===

Pre-Flood Preparation:
- Identify main circuit breaker location (know how to shut off quickly)
- Move electronics to upper floors or raise on blocks
- Unplug all non-essential appliances during heavy rain warnings
- Backup power: Consider portable generators for critical medical equipment (use outdoors only)

During Flooding:
- Turn off main power if water enters home (do not walk through water to do so)
- Never touch electrical equipment if wet or standing in water
- If wires fall into standing water, evacuate immediately
- Avoid using landline phones during thunderstorms (lightning risk via lines)

Post-Flood Restoration:
- Have licensed electrician inspect system before restoring power
- Replace all electrical outlets that were submerged
- Discard appliances that were underwater (fire hazard)
- Check for gas leaks if LPG used (pilot lights may extinguish)

=== Insurance Coverage ===

Types of Coverage:
- Home Contents Insurance: Covers personal belongings (furniture, electronics)
- Building Insurance: Covers structure (for private property owners)
- Fire Insurance (HDB): Mandatory but limited coverage, usually excludes flood
- Comprehensive Home Insurance: Includes flood, theft, accidental damage

Flood-Specific Clauses:
- Check "Acts of God" or "Natural Disasters" sections
- Note exclusions for gradual seepage vs. sudden flooding
- Understand deductible amounts (excess)
- Confirm coverage for alternative accommodation during repairs

Documentation for Claims:
- Photograph/video property condition before monsoon season
- Keep receipts for high-value items (scanned copies in cloud)
- Document flood damage immediately (date-stamped photos)
- Obtain police reports for major flooding events
- Keep records of all mitigation expenses (sandbags, pumps, etc.)

Claim Process:
1. Notify insurer within 24 hours (most require immediate reporting)
2. Prevent further damage (mitigation duty)
3. Inventory damaged items (model numbers, purchase dates)
4. Obtain repair quotes from approved contractors
5. Cooperate with loss adjusters inspection

Common Exclusions:
- Damage from lack of maintenance (blocked drains on property)
- Unoccupied properties (>30 days empty)
- Basement contents unless specifically declared
- Construction materials (if renovating during flood)

=== Business Continuity ===

For Retail/Commercial Tenants:
- Inventory management: Raise stock 15cm minimum during monsoon
- Electronic point-of-sale systems: Portable, can move to safety
- Document storage: Cloud-based, waterproof safes for originals
- Business interruption insurance: Covers lost income during closure

For Offices:
- Server rooms: Locate above ground floor, waterproof raised flooring
- Work-from-home protocols: Activated when flood warnings issued
- Critical documents: Waterproof fire safes, offsite backups
- Client communication: Automated systems to notify of closure

Supply Chain Considerations:
- Identify alternative suppliers outside flood zones
- 72-hour inventory buffer for critical stock
- Waterproof packaging for stored goods
- Delivery route planning avoiding flood-prone roads

=== Emergency Kits for Properties ===

Home Emergency Kit:
- Portable radio (battery or hand-crank)
- First aid kit (waterproof container)
- Torches and extra batteries
- Important documents (waterproof bag): IC, passports, insurance policies, property deeds
- Medications (7-day supply)
- Bottled water (4 liters per person per day)
- Non-perishable food (3-day supply)
- Cash (ATMs may be down)
- Whistle (to signal for help)

Business Emergency Kit:
- Contact lists (employees, suppliers, customers)
- Backup drives with critical data
- Emergency signage (closure notices)
- Cleaning supplies (mops, buckets, disinfectant)
- Wet/dry vacuum (shop vac for water removal)
- Dehumidifiers (prevent mold growth)

=== Recovery and Remediation ===

Immediate Actions (First 24 Hours):
- Document everything (photos for insurance)
- Remove water quickly (mold grows within 48 hours)
- Salvage valuables (prioritize documents, electronics)
- Contact insurance company
- Notify landlord if tenant

Drying Out Process:
- Industrial fans and dehumidifiers (rent from Home-Fix or similar)
- Remove wet carpets and underlay (usually cannot be saved)
- Cut drywall 15cm above water line (prevents wicking)
- Dispose of contaminated insulation
- Clean all hard surfaces with bleach solution (1:10 ratio)

Mold Prevention:
- Keep humidity below 60%
- Run air conditioning continuously initially
- Inspect behind walls and under floors
- Professional mold assessment if musty odors persist
- Health symptoms (respiratory) indicate hidden mold

Long-Term Recovery:
- Structural assessment by professional engineer
- Electrical system certification
- Pest control (flood displaces rodents and insects)
- Landscape restoration (prevent erosion)
- Update emergency plans based on lessons learned

=== Contact Numbers ===

Insurance Claims (Major Providers):
- AIA: 1800-226-0300
- NTUC Income: 6788-1777
- Great Eastern: 1800-248-2888
- Prudential: 1800-333-0333
- AXA: 1800-880-4888

Government Agencies:
- PUB (Flooding Issues): 1800-CALL-PUB
- SCDF (Rescue): 995
- HDB (Estate Issues): 1800-225-5432
- BCA (Building Safety): 1800-342-5225
- Town Councils: Check notice board for local number

Emergency Services:
- Police: 999
- Ambulance/Rescue: 995
- Non-emergency Police: 1800-255-0000"""
}

# Create all files
import os

created_files = []
for filename, content in files_content.items():
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    created_files.append(filename)
    print(f"✓ Created: {filename}")

print(f"\n✅ Successfully created {len(created_files)} files in: {os.getcwd()}")
print("\nFiles created:")
for i, file in enumerate(created_files, 1):
    print(f"{i:2d}. {file}")