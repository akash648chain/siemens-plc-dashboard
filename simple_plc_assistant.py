#!/usr/bin/env python3
"""
Simplified Siemens PLC QA Assistant without complex transformer dependencies
"""

import os
import json
from typing import List, Dict, Any
from pathlib import Path
import re

class SimplePLCQAAssistant:
    def __init__(self):
        self.knowledge_base = []
        self.initialize_knowledge()
    
    def initialize_knowledge(self):
        """Initialize the PLC knowledge base"""
        self.knowledge_base = [
            {
                "title": "Siemens S7-1500 Overview",
                "keywords": ["s7-1500", "s7 1500", "simatic s7-1500", "cpu 1500", "plc 1500"],
                "content": """
                The Siemens S7-1500 is a high-performance PLC system for demanding automation tasks.
                
                Key Features:
                - Modular design with scalable I/O
                - Integrated PROFINET interface
                - High-speed processing (up to 1 μs bit operations)
                - Integrated web server for diagnostics
                - Support for motion control and safety functions
                - TIA Portal programming environment
                - Memory: up to 5 MB work memory, 2 GB load memory
                - Communication: PROFINET, PROFIBUS, Ethernet
                
                Applications: Complex automation tasks, process control, motion control, safety applications
                """
            },
            {
                "title": "Siemens S7-1200 Overview", 
                "keywords": ["s7-1200", "s7 1200", "simatic s7-1200", "cpu 1200", "plc 1200"],
                "content": """
                The Siemens S7-1200 is a compact PLC for small to medium automation applications.
                
                Key Features:
                - Compact design with integrated I/O
                - Built-in PROFINET and Ethernet ports
                - Integrated analog inputs and outputs
                - Pulse outputs for basic motion control
                - Communication modules for serial interfaces
                - TIA Portal programming
                - Memory: up to 100 KB work memory, 4 MB load memory
                - Real-time clock and calendar functions
                
                Applications: Machine control, small automation systems, building automation
                """
            },
            {
                "title": "TIA Portal Programming",
                "keywords": ["tia portal", "tia", "programming", "ladder", "fbd", "stl", "scl", "graph"],
                "content": """
                TIA Portal (Totally Integrated Automation Portal) is Siemens' integrated engineering software.
                
                Programming Languages:
                - LAD (Ladder Logic): Graphical representation similar to electrical relay circuits
                - FBD (Function Block Diagram): Uses function blocks connected by signal lines
                - STL (Statement List): Text-based instruction list programming
                - SCL (Structured Control Language): High-level programming language similar to Pascal
                - GRAPH (Sequential Function Chart): For sequential control processes
                
                Key Features:
                - Integrated development environment
                - Hardware configuration and parameterization
                - Simulation capabilities (PLCSIM)
                - Version control and project management
                - Library management for reusable code
                - Online diagnostics and monitoring
                - Cross-reference and dependency analysis
                """
            },
            {
                "title": "PROFINET Communication",
                "keywords": ["profinet", "communication", "ethernet", "industrial ethernet", "rt", "irt"],
                "content": """
                PROFINET is Siemens' industrial Ethernet standard for automation.
                
                Types:
                - PROFINET RT (Real-Time): Standard real-time communication
                - PROFINET IRT (Isochronous Real-Time): Deterministic, synchronized communication
                
                Features:
                - Based on standard Ethernet (IEEE 802.3)
                - Integration with existing IT infrastructure
                - Hot-swappable devices
                - Automatic device detection and configuration
                - Distributed I/O systems
                - Motion control integration
                - Comprehensive diagnostics
                
                Configuration:
                1. Hardware configuration in TIA Portal
                2. Assign IP addresses to devices
                3. Configure communication parameters
                4. Download configuration to PLC
                """
            },
            {
                "title": "Safety Functions",
                "keywords": ["safety", "fail-safe", "sil", "ple", "emergency stop", "light curtain", "f-cpu"],
                "content": """
                Siemens PLCs support integrated safety functions through Safety Integrated technology.
                
                Safety Levels:
                - SIL 3 (Safety Integrity Level 3)
                - PLe (Performance Level e)
                
                Components:
                - F-CPU: Fail-safe CPU modules
                - F-I/O: Fail-safe input/output modules
                - Safety programming in TIA Portal
                
                Applications:
                - Emergency stop circuits
                - Light curtain monitoring
                - Two-hand control
                - Safety door monitoring
                - Speed and standstill monitoring
                
                Programming:
                - F-FBD (Fail-safe Function Block Diagram)
                - F-LAD (Fail-safe Ladder Diagram)
                - Safety libraries and function blocks
                """
            },
            {
                "title": "Data Blocks and Memory",
                "keywords": ["data block", "db", "memory", "global db", "instance db", "optimized", "retain"],
                "content": """
                Siemens PLC memory organization and data storage.
                
                Memory Areas:
                - I (Input): Process input image
                - Q (Output): Process output image  
                - M (Memory): Bit memory for internal data
                - DB (Data Block): Structured data storage
                
                Data Block Types:
                - Global DB: Accessible by all program blocks
                - Instance DB: Associated with specific function blocks
                - Optimized DB: Allows symbolic access, better performance
                - Non-optimized DB: Absolute addressing, compatible with older systems
                
                Memory Management:
                - Retain memory: Data preserved during power loss
                - Load memory: Stores program code and configuration
                - Work memory: Runtime execution memory
                
                Best Practices:
                - Use optimized data blocks for new projects
                - Implement proper data structure organization
                - Consider memory limits when designing applications
                """
            },
            {
                "title": "Communication Troubleshooting",
                "keywords": ["communication error", "profinet error", "network error", "connection lost", "timeout", "ethernet", "profibus"],
                "content": """
                Comprehensive guide for Siemens PLC communication troubleshooting.
                
                PROFINET Communication Errors:
                - Error 16#8087: Device not reachable
                  Solution: Check IP configuration, network cables, switch settings
                - Error 16#8088: Communication timeout
                  Solution: Verify cycle times, reduce network load, check diagnostics
                - Error 16#808A: Station failure
                  Solution: Check device power, firmware version, replace device if necessary
                
                Ethernet Communication Issues:
                - IP address conflicts: Use PRONETA to scan network
                - Subnet mask mismatch: Verify all devices use same subnet
                - Switch configuration: Check VLAN settings, port configuration
                - Cable issues: Test with known good cables, check connector crimping
                
                PROFIBUS Troubleshooting:
                - Bus termination: Ensure proper 220Ω termination at both ends
                - Baud rate mismatch: Verify all devices use same baud rate
                - Address conflicts: Check for duplicate station addresses
                - Cable quality: Use specified PROFIBUS cable (Type A/B)
                
                Diagnostic Tools:
                - TIA Portal online diagnostics
                - PRONETA network scanner
                - PROFIBUS tester for bus analysis
                - Wireshark for Ethernet packet analysis
                """
            },
            {
                "title": "CPU Hardware Faults",
                "keywords": ["cpu fault", "hardware error", "led indicators", "stop mode", "cpu error", "rack error"],
                "content": """
                Siemens CPU hardware fault diagnosis and solutions.
                
                LED Indicator Meanings:
                - RUN (Green): CPU in normal operation
                - STOP (Yellow): CPU stopped, check program or hardware
                - ERROR (Red): Hardware fault, check diagnostics buffer
                - MAINT (Yellow): Maintenance required, firmware update needed
                
                Common CPU Errors:
                - Memory card error: Check SD card insertion, format if necessary
                - Battery fault: Replace backup battery (CR2032)
                - Overtemperature: Check ventilation, clean dust filters
                - Power supply issues: Verify 24V DC supply, check voltage levels
                
                Diagnostics Buffer Errors:
                - Event ID 16#3501: Memory card removed during operation
                - Event ID 16#3502: Memory card write error
                - Event ID 16#4001: Power failure detected
                - Event ID 16#4004: Battery voltage low
                
                Recovery Procedures:
                - Memory reset: Hold MRES for 3 seconds
                - Factory reset: MRES for 3-6 seconds in STOP mode
                - Firmware update: Use TIA Portal automation software updater
                - Configuration restore: Load backup from memory card
                
                Preventive Maintenance:
                - Regular backup of program and configuration
                - Battery replacement every 5 years
                - Firmware updates for security patches
                - Dust cleaning and ventilation check
                """
            },
            {
                "title": "I/O Module Troubleshooting",
                "keywords": ["io error", "input error", "output error", "module fault", "signal fault", "wiring error"],
                "content": """
                Input/Output module troubleshooting for Siemens PLCs.
                
                Digital I/O Problems:
                - Input not reading: Check 24V supply, wiring, sensor power
                - Output not switching: Verify load connection, fuse status, output LED
                - Intermittent signals: Check loose connections, electromagnetic interference
                - Wrong logic level: Verify PNP/NPN sensor configuration
                
                Analog I/O Issues:
                - Measurement out of range: Check sensor calibration, scaling parameters
                - Noisy signals: Use shielded cables, separate power and signal cables
                - Offset errors: Perform module calibration, check reference voltage
                - Temperature drift: Verify ambient temperature, use compensation
                
                Module Status LEDs:
                - SF (Red): Module fault, check diagnostics
                - BF (Red): Bus fault, check backplane connection
                - Channel LEDs: Individual channel status indicators
                
                Common Error Codes:
                - 16#8000: General module error
                - 16#8001: Configuration error
                - 16#8004: Channel fault
                - 16#8090: Wire break detection
                
                Troubleshooting Steps:
                1. Check module LED status
                2. Verify hardware configuration in TIA Portal
                3. Test with force tables for outputs
                4. Measure voltages at terminal blocks
                5. Replace module if hardware fault confirmed
                
                Wiring Best Practices:
                - Use proper cable types (shielded for analog)
                - Maintain separation between power and signal cables
                - Check torque specifications for terminals
                - Label all connections for maintenance
                """
            },
            {
                "title": "Programming Errors & Debugging",
                "keywords": ["programming error", "runtime error", "logic error", "debugging", "monitoring", "force tables"],
                "content": """
                Common programming errors and debugging techniques in TIA Portal.
                
                Runtime Errors:
                - Division by zero: Add zero check before division operations
                - Array index out of bounds: Validate array indices
                - Data type mismatch: Ensure compatible data types in operations
                - Timer/Counter overflow: Monitor timer values and reset appropriately
                
                Logic Errors:
                - Incorrect operator precedence: Use parentheses for clarity
                - Missing edge detection: Use rising/falling edge instructions
                - Infinite loops: Add loop counters and exit conditions
                - Memory leaks: Properly manage dynamic memory allocation
                
                Debugging Tools in TIA Portal:
                - Online monitoring: Watch variable values in real-time
                - Force tables: Manually set input/output values for testing
                - Trace function: Record variable changes over time
                - Breakpoints: Pause execution at specific points
                
                Common Programming Mistakes:
                - Using non-retain memory for critical data
                - Inadequate error handling in communication blocks
                - Missing initialization of variables
                - Improper use of system functions
                
                Best Practices:
                - Use symbolic addressing instead of absolute
                - Implement proper error handling
                - Comment code thoroughly
                - Use structured programming with functions and function blocks
                - Test all code paths before deployment
                
                Performance Optimization:
                - Minimize scan time by optimizing program structure
                - Use interrupt routines for time-critical operations
                - Reduce communication overhead
                - Monitor CPU load and cycle time
                """
            },
            {
                "title": "Safety System Troubleshooting",
                "keywords": ["safety error", "f-cpu", "fail-safe", "emergency stop", "light curtain", "safety io", "sil"],
                "content": """
                Safety system troubleshooting for Siemens Safety Integrated.
                
                F-CPU Specific Errors:
                - Safety program error: Check F-program compilation
                - Safety signature mismatch: Re-generate safety signatures
                - Safety time exceeded: Review safety cycle time settings
                - Fail-safe channel fault: Check F-I/O module connections
                
                Emergency Stop Circuit Issues:
                - E-stop not detected: Verify contact configuration (NC contacts)
                - Safety relay not responding: Check relay coil and contacts
                - Reset not working: Verify reset button wiring and logic
                - Monitoring time too short: Adjust safety function parameters
                
                Light Curtain Problems:
                - Muting not working: Check muting sensor alignment
                - False trips: Verify beam pattern and environmental conditions
                - Communication error: Check safety bus connection
                - Response time too slow: Review safety system configuration
                
                Safety I/O Diagnostics:
                - Channel error: Check sensor power supply and wiring
                - Discrepancy error: Verify dual-channel sensor connections
                - Test pulse error: Check F-I/O module function
                - Cross-circuit fault: Isolate channels and test individually
                
                Safety Validation:
                - Functional safety test: Regular testing per safety standards
                - Documentation: Maintain safety function documentation
                - Proof test: Periodic testing of safety functions
                - Risk assessment: Regular review of safety requirements
                
                Compliance Requirements:
                - IEC 61508: Functional safety standard
                - ISO 13849: Safety of machinery standard
                - Regular safety audits and certifications
                - Training for safety system maintenance
                """
            },
            {
                "title": "Motion Control Troubleshooting",
                "keywords": ["motion control", "servo error", "drive fault", "encoder error", "positioning error", "sinamics"],
                "content": """
                Motion control and drive troubleshooting for Siemens systems.
                
                SINAMICS Drive Faults:
                - F7902: Encoder error - Check encoder cable and connections
                - F7121: Motor overtemperature - Check cooling and motor load
                - F7011: Overcurrent fault - Verify motor parameters and load
                - F30005: Power supply fault - Check DC bus voltage
                
                Positioning Errors:
                - Following error too large: Tune servo parameters (Kp, Ki, Kd)
                - Target not reached: Check mechanical binding, encoder resolution
                - Oscillation: Reduce gain parameters, add damping
                - Overshoot: Adjust acceleration/deceleration ramps
                
                Encoder Problems:
                - Signal loss: Check cable continuity and shielding
                - Count error: Verify encoder type and resolution settings
                - Noise interference: Use proper cable routing and grounding
                - Reference point lost: Re-establish home position
                
                Communication Issues:
                - PROFINET RT for motion: Check cycle times and QoS settings
                - Drive telegram errors: Verify telegram configuration
                - Synchronization problems: Check isochronous mode settings
                - Safety integration: Verify STO (Safe Torque Off) connections
                
                Commissioning Tools:
                - STARTER software for SINAMICS drives
                - TIA Portal motion control configuration
                - Drive oscilloscope for signal analysis
                - Mechanical vibration analysis
                
                Preventive Maintenance:
                - Regular encoder cleaning and inspection
                - Drive cooling system maintenance
                - Cable inspection for wear and damage
                - Parameter backup and documentation
                """
            },
            {
                "title": "HMI and Visualization Issues",
                "keywords": ["hmi error", "wincc", "visualization", "screen problem", "touch error", "communication hmi"],
                "content": """
                HMI and visualization troubleshooting for Siemens panels.
                
                HMI Communication Errors:
                - Connection timeout: Check Ethernet settings and cable
                - Variable not updating: Verify tag configuration and scaling
                - Slow response: Optimize communication settings, reduce update rates
                - Authentication failed: Check user management and passwords
                
                Touch Panel Problems:
                - Touch not responding: Calibrate touch screen, check for damage
                - Display issues: Adjust brightness, check backlight
                - Memory full: Clear logs, optimize project size
                - Performance slow: Reduce graphic complexity, optimize animations
                
                WinCC Runtime Errors:
                - License error: Verify WinCC runtime license
                - Script error: Debug VB scripts, check syntax
                - Database connection: Verify SQL server connection
                - Alarm not triggered: Check alarm class configuration
                
                Common Solutions:
                - Project transfer failed: Check communication settings
                - Recipe management: Verify recipe structure and data types
                - Trend display: Optimize archive configuration
                - User management: Check role and permission settings
                
                Best Practices:
                - Regular backup of HMI project
                - Monitor system resources (CPU, memory)
                - Use consistent naming conventions
                - Implement proper error handling in scripts
                - Test all operator functions before deployment
                
                Performance Optimization:
                - Minimize number of variables in communication
                - Use appropriate update cycles for different data
                - Optimize graphics and animations
                - Regular maintenance of HMI hardware
                """
            },
            {
                "title": "Network and IT Integration",
                "keywords": ["network error", "firewall", "security", "remote access", "vpn", "industrial security"],
                "content": """
                Network integration and IT security for Siemens automation systems.
                
                Firewall Configuration:
                - Port requirements: Open necessary ports for PROFINET, HTTP, HTTPS
                - Deep packet inspection: Configure for industrial protocols
                - VPN access: Set up secure remote access tunnels
                - Network segmentation: Isolate OT from IT networks
                
                Industrial Security:
                - Password policy: Implement strong password requirements
                - Certificate management: Use X.509 certificates for authentication
                - Access control: Implement role-based access control
                - Audit logging: Enable security event logging
                
                Remote Access Issues:
                - VPN connection problems: Check VPN client configuration
                - Slow remote performance: Optimize bandwidth usage
                - Authentication failures: Verify user credentials and certificates
                - Session timeouts: Adjust timeout settings appropriately
                
                Common Network Problems:
                - DHCP conflicts: Use static IP addresses for critical devices
                - DNS resolution: Configure proper DNS settings
                - Time synchronization: Implement NTP for accurate time
                - Bandwidth limitations: Monitor and manage network traffic
                
                Best Practices:
                - Regular security updates and patches
                - Network monitoring and intrusion detection
                - Backup and disaster recovery planning
                - Documentation of network architecture
                - Staff training on cybersecurity
                
                Compliance Standards:
                - IEC 62443: Industrial cybersecurity standards
                - NIST Framework: Cybersecurity framework implementation
                - Regular security assessments and penetration testing
                - Incident response procedures
                """
            },
            {
                "title": "Specific Error Codes and Solutions",
                "keywords": ["error code", "fault code", "diagnostic", "8087", "8088", "808A", "3501", "4001", "F7902", "F7121"],
                "content": """
                Common Siemens error codes with specific solutions.
                
                Communication Error Codes:
                - 16#8087 (Device not reachable):
                  * Check physical network connection
                  * Verify IP address configuration
                  * Check switch/router settings
                  * Test with ping command
                  * Verify PROFINET device status
                
                - 16#8088 (Communication timeout):
                  * Reduce update cycles in HMI/SCADA
                  * Check network load and bandwidth
                  * Verify CPU cycle time settings
                  * Optimize communication parameters
                  * Check for electromagnetic interference
                
                - 16#808A (Station failure):
                  * Check device power supply
                  * Verify firmware compatibility
                  * Replace faulty network components
                  * Check for hardware defects
                  * Validate device configuration
                
                CPU Diagnostic Events:
                - 16#3501 (Memory card removed):
                  * Re-insert memory card properly
                  * Check card compatibility
                  * Format card if corrupted
                  * Verify card lock mechanism
                
                - 16#4001 (Power failure detected):
                  * Check 24V power supply stability
                  * Verify backup battery status
                  * Check power supply connections
                  * Implement UPS if necessary
                
                - 16#4004 (Battery voltage low):
                  * Replace CR2032 backup battery
                  * Check battery holder contacts
                  * Verify battery insertion orientation
                  * Test new battery voltage (3.0-3.6V)
                
                Drive Fault Codes (SINAMICS):
                - F7902 (Encoder fault):
                  * Check encoder cable for damage
                  * Verify encoder power supply (5V/15V)
                  * Test encoder signals with oscilloscope
                  * Replace encoder if faulty
                
                - F7121 (Motor overtemperature):
                  * Check motor cooling system
                  * Verify thermal sensor connections
                  * Reduce motor load or speed
                  * Check ambient temperature
                
                - F7011 (Overcurrent fault):
                  * Check motor parameters in drive
                  * Verify load conditions
                  * Check for mechanical binding
                  * Inspect motor insulation
                """
            },
            {
                "title": "Common Google Search Problems",
                "keywords": ["siemens plc not starting", "tia portal connection", "profinet not working", "hmi not connecting", "memory card error"],
                "content": """
                Solutions to frequently searched Siemens PLC problems.
                
                'Siemens PLC not starting' Issues:
                - Check power supply (24V DC, proper grounding)
                - Verify memory card insertion and format
                - Review CPU LED indicators for error status
                - Check for loose connections in power circuits
                - Verify program download and configuration
                - Test with minimal configuration first
                
                'TIA Portal cannot connect to PLC':
                - Verify IP address settings match PLC configuration
                - Check Windows firewall settings (disable temporarily)
                - Ensure correct PG/PC interface selection
                - Test network connectivity with ping
                - Verify Ethernet cable and network adapter
                - Check if another TIA Portal session is active
                
                'PROFINET device not detected':
                - Use PRONETA to scan network for devices
                - Check device IP address and subnet configuration
                - Verify PROFINET cable quality (Cat5e/Cat6)
                - Reset device to factory defaults if necessary
                - Check switch configuration and VLAN settings
                - Verify device naming and topology
                
                'HMI cannot connect to PLC':
                - Check HMI connection configuration
                - Verify PLC allows HMI communication
                - Test communication with simple variables first
                - Check user permissions and access rights
                - Verify HMI runtime license
                - Review communication driver settings
                
                'Memory card error' Solutions:
                - Format card using TIA Portal (not Windows)
                - Check card compatibility (Siemens approved cards)
                - Verify proper insertion (card should click)
                - Test with different memory card
                - Check for physical damage on card or slot
                - Ensure card is not write-protected
                
                'CPU goes to STOP mode randomly':
                - Check for watchdog timer violations
                - Review scan time and cycle monitoring
                - Look for infinite loops in program
                - Check for division by zero errors
                - Verify array bounds in program logic
                - Monitor CPU load and memory usage
                """
            },
            {
                "title": "Performance and Optimization",
                "keywords": ["slow performance", "cpu load", "scan time", "optimization", "memory usage", "cycle time"],
                "content": """
                Performance optimization for Siemens PLC systems.
                
                CPU Performance Issues:
                - High scan time: Optimize program structure, reduce unnecessary calculations
                - Memory shortage: Clean up unused variables, optimize data structures
                - Communication overload: Reduce update rates, optimize data exchange
                - Interrupt conflicts: Review interrupt priorities and timing
                
                Programming Optimization:
                - Use efficient data types (BOOL vs BYTE vs WORD)
                - Minimize floating-point operations
                - Optimize loop structures and conditional statements
                - Use lookup tables instead of complex calculations
                - Implement proper program organization (OBs, FCs, FBs)
                
                Communication Optimization:
                - Reduce PROFINET update cycles where possible
                - Group related I/O data in communication
                - Use appropriate communication protocols
                - Implement communication error handling
                - Monitor network bandwidth usage
                
                HMI Performance:
                - Limit number of variables in trends and faceplates
                - Optimize screen update cycles
                - Reduce graphic complexity and animations
                - Implement proper caching strategies
                - Use appropriate data archive settings
                
                Diagnostic and Monitoring:
                - Regular system performance monitoring
                - Trend analysis of CPU load and memory usage
                - Network traffic analysis and optimization
                - Preventive maintenance scheduling
                - Documentation of system changes
                
                Best Practices:
                - Regular backup of all project components
                - Version control for program changes
                - Performance baseline establishment
                - Capacity planning for future expansion
                - Staff training on optimization techniques
                """
            },
            {
                "title": "Ladder Logic Programming Examples",
                "keywords": ["ladder logic", "lad", "programming examples", "ladder diagram", "contacts", "coils", "rungs"],
                "content": """
                Comprehensive ladder logic programming examples for learning and troubleshooting.
                
                Basic Ladder Logic Elements:
                ┌─── Normally Open Contact (NO) ───┐
                │ ──┤ I0.0 ├── │
                └─── Input Signal ───┘
                
                ┌─── Normally Closed Contact (NC) ───┐
                │ ──┤/I0.1├── │
                └─── Inverted Input Signal ───┘
                
                ┌─── Output Coil ───┐
                │ ──( Q0.0 )── │
                └─── Output Assignment ───┘
                
                Example 1: Simple Start/Stop Circuit
                Network 1: Motor Control
                ──┤ Start ├──┤/Stop ├──┤ Motor_Running ├──( Motor )──
                │  I0.0    │  I0.1   │     M0.0       │   Q0.0
                │          │         │                │
                └──────────┴─────────┘                │
                                                      │
                ──┤ Motor ├──────────────────────────( Motor_Running )──
                   Q0.0                                    M0.0
                
                Explanation:
                - Start button (I0.0) initiates motor
                - Stop button (I0.1) NC contact stops motor
                - Motor_Running (M0.0) provides latching
                - Motor output (Q0.0) controls actual motor
                
                Example 2: Timer-Based Sequence
                Network 1: Start Timer
                ──┤ Start ├──┤/Reset ├──( TON_Timer )──
                   I0.0       I0.1        T1
                                         PT: T#10s
                
                Network 2: Timer Output
                ──┤ T1.Q ├──( Output )──
                   Timer     Q0.0
                
                Example 3: Counter Application
                Network 1: Count Pulses
                ──┤ Sensor ├──┤/Reset ├──( CTU_Counter )──
                   I0.0        I0.1        C1
                                          PV: 10
                
                Network 2: Counter Output
                ──┤ C1.Q ├──( Alarm )──
                   Counter    Q0.1
                """
            },
            {
                "title": "Advanced Ladder Logic Patterns",
                "keywords": ["advanced ladder", "function blocks", "fb", "fc", "data blocks", "structured programming"],
                "content": """
                Advanced ladder logic programming patterns and best practices.
                
                Function Block (FB) Example: Motor Control
                FB1 "Motor_Control"
                
                Input Parameters:
                - Start (BOOL): Start command
                - Stop (BOOL): Stop command
                - Emergency (BOOL): Emergency stop
                - Feedback (BOOL): Motor feedback signal
                
                Output Parameters:
                - Motor_On (BOOL): Motor output
                - Fault (BOOL): Fault indication
                - Runtime (TIME): Operating time
                
                Internal Logic:
                Network 1: Safety Check
                ──┤/Emergency ├──┤ Feedback ├──( Safety_OK )──
                   %I           %I             %M0.0
                
                Network 2: Motor Control
                ──┤ Start ├──┤/Stop ├──┤ Safety_OK ├──┤ Motor_On ├──( Motor_On )──
                   %I         %I       %M0.0        %Q           %Q
                
                Network 3: Fault Detection
                ──┤ Motor_On ├──┤/Feedback ├──( TON_Fault )──
                   %Q          %I              T1, PT: T#5s
                
                ──┤ T1.Q ├──( Fault )──
                   Timer     %Q
                
                Function (FC) Example: Scaling
                FC1 "Analog_Scale"
                
                Input: Raw_Value (INT), Min_Raw (INT), Max_Raw (INT)
                Output: Scaled_Value (REAL), Min_Scale (REAL), Max_Scale (REAL)
                
                Calculation:
                Scaled_Value := (Raw_Value - Min_Raw) * (Max_Scale - Min_Scale) / (Max_Raw - Min_Raw) + Min_Scale
                
                Example Usage:
                Network 1: Temperature Scaling
                ──[ CALL FC1 ]──
                   Raw_Value := AI_Temperature
                   Min_Raw := 0
                   Max_Raw := 27648
                   Min_Scale := 0.0
                   Max_Scale := 100.0
                   Scaled_Value => Temperature_Celsius
                """
            },
            {
                "title": "Ladder Logic Troubleshooting Guide",
                "keywords": ["ladder troubleshooting", "debugging ladder", "program errors", "logic errors", "monitoring"],
                "content": """
                Comprehensive troubleshooting guide for ladder logic programs.
                
                Common Ladder Logic Errors:
                
                1. Missing Latch/Unlatch Logic:
                Problem: Output doesn't stay on after momentary input
                
                Incorrect:
                ──┤ Start ├──( Motor )──
                   I0.0       Q0.0
                
                Correct:
                ──┤ Start ├──┤/Stop ├──┤ Motor ├──( Motor )──
                   I0.0       I0.1      Q0.0      Q0.0
                
                2. Contact vs Coil Confusion:
                Problem: Using output coil instead of contact for logic
                
                Incorrect:
                ──┤ Input ├──( Output )──┤ Output ├──( Next_Output )──
                   I0.0       Q0.0        Q0.0       Q0.1
                
                Correct:
                ──┤ Input ├──( Output )──
                   I0.0       Q0.0
                ──┤ Output ├──( Next_Output )──
                   Q0.0        Q0.1
                
                3. Timer Programming Issues:
                Problem: Timer doesn't reset properly
                
                Incorrect:
                ──┤ Start ├──( TON_Timer )──
                   I0.0       T1, PT: T#10s
                
                Correct:
                ──┤ Start ├──┤/Reset ├──( TON_Timer )──
                   I0.0       I0.1        T1, PT: T#10s
                
                4. Counter Issues:
                Problem: Counter doesn't count properly
                
                Check:
                - Rising edge detection for count input
                - Proper reset logic
                - Preset value settings
                
                Debugging Techniques:
                
                1. Online Monitoring:
                - Watch contact states (green = TRUE, white = FALSE)
                - Monitor coil states and values
                - Check timer/counter current values
                
                2. Force Tables:
                - Force inputs to test logic paths
                - Force outputs to test hardware
                - Use with caution in live systems
                
                3. Cross-Reference Lists:
                - Find all uses of variables
                - Check for multiple coil assignments
                - Verify data consistency
                
                4. Simulation Mode:
                - Test logic without hardware
                - Verify program flow
                - Check edge cases
                
                Common Troubleshooting Steps:
                1. Check power supply to I/O modules
                2. Verify input signal presence with multimeter
                3. Test outputs with force tables
                4. Monitor program execution online
                5. Check for conflicting logic
                6. Verify timer/counter parameters
                7. Test emergency stops and safety circuits
                """
            },
            {
                "title": "Practical Ladder Logic Examples",
                "keywords": ["conveyor control", "traffic light", "pump control", "sequential control", "practical examples"],
                "content": """
                Real-world ladder logic examples for learning and reference.
                
                Example 1: Conveyor Belt Control System
                
                Inputs:
                I0.0 - Start Button
                I0.1 - Stop Button (NC)
                I0.2 - Emergency Stop (NC)
                I0.3 - Product Sensor
                I0.4 - End Position Sensor
                
                Outputs:
                Q0.0 - Conveyor Motor
                Q0.1 - Warning Light
                Q0.2 - Counter Display
                
                Network 1: Safety Circuit
                ──┤/Emergency ├──( Safety_OK )──
                   I0.2          M0.0
                
                Network 2: Conveyor Control
                ──┤ Start ├──┤/Stop ├──┤ Safety_OK ├──┤ Conveyor ├──( Conveyor )──
                   I0.0       I0.1      M0.0         Q0.0        Q0.0
                
                Network 3: Product Counter
                ──┤ Product_Sensor ├──┤ Conveyor ├──( CTU_Products )──
                   I0.3              Q0.0          C1, PV: 100
                
                Network 4: Warning Light
                ──┤ C1.Q ├──( Warning )──
                   Counter   Q0.1
                
                Example 2: Three-Phase Motor Starter
                
                Inputs:
                I0.0 - Start Button (NO)
                I0.1 - Stop Button (NC)
                I0.2 - Overload Relay (NC)
                I0.3 - Motor Contactor Auxiliary (NO)
                
                Outputs:
                Q0.0 - Motor Contactor
                Q0.1 - Run Indicator
                Q0.2 - Fault Indicator
                
                Network 1: Motor Control Circuit
                ──┤ Start ├──┤/Stop ├──┤/Overload ├──┤ Run ├──( Motor_Contactor )──
                   I0.0       I0.1      I0.2         Q0.0    Q0.0
                
                Network 2: Run Indicator
                ──┤ Motor_Contactor ├──( Run_Light )──
                   Q0.0                  Q0.1
                
                Network 3: Fault Detection
                ──┤ Motor_Contactor ├──┤/Motor_Aux ├──( TON_Fault )──
                   Q0.0                  I0.3          T1, PT: T#2s
                
                ──┤ T1.Q ├──┤/Overload ├──( Fault_Light )──
                   Timer     I0.2         Q0.2
                
                Example 3: Automatic Door Control
                
                Inputs:
                I0.0 - Open Button
                I0.1 - Close Button
                I0.2 - Door Fully Open Limit
                I0.3 - Door Fully Closed Limit
                I0.4 - Safety Beam
                
                Outputs:
                Q0.0 - Door Open Motor
                Q0.1 - Door Close Motor
                Q0.2 - Door Open Light
                Q0.3 - Door Closed Light
                
                Network 1: Open Door
                ──┤ Open_Button ├──┤/Door_Open ├──┤ Safety_Beam ├──( Open_Motor )──
                   I0.0            I0.2          I0.4            Q0.0
                
                Network 2: Close Door
                ──┤ Close_Button ├──┤/Door_Closed ├──┤ Safety_Beam ├──( Close_Motor )──
                   I0.1             I0.3            I0.4             Q0.1
                
                Network 3: Interlock (Prevent Both Motors)
                ──┤ Close_Motor ├──┤/Open_Motor ├──( Open_Motor )──
                   Q0.1            Q0.0           Q0.0
                
                Network 4: Status Lights
                ──┤ Door_Open ├──( Open_Light )──
                   I0.2          Q0.2
                
                ──┤ Door_Closed ├──( Closed_Light )──
                   I0.3            Q0.3
                """
            },
            {
                "title": "Safety Ladder Logic Programming",
                "keywords": ["safety ladder", "emergency stop", "safety circuits", "fail-safe", "category 3", "category 4"],
                "content": """
                Safety-oriented ladder logic programming with fail-safe principles.
                
                Emergency Stop Circuit (Category 3):
                
                Inputs:
                I0.0 - Start Button (NO)
                I0.1 - Emergency Stop 1 (NC)
                I0.2 - Emergency Stop 2 (NC)
                I0.3 - Safety Gate (NC)
                I0.4 - Reset Button (NO)
                I0.5 - Safety Relay Feedback (NO)
                
                Outputs:
                Q0.0 - Safety Relay Coil
                Q0.1 - Machine Enable
                Q0.2 - Fault Indicator
                
                Network 1: Safety Logic
                ──┤/E_Stop1 ├──┤/E_Stop2 ├──┤/Safety_Gate ├──( Safety_Chain )──
                   I0.1         I0.2         I0.3            M0.0
                
                Network 2: Safety Relay Control
                ──┤ Reset ├──┤ Safety_Chain ├──┤ Safety_Feedback ├──( Safety_Relay )──
                   I0.4       M0.0            I0.5               Q0.0
                
                Network 3: Machine Enable
                ──┤ Start ├──┤ Safety_Relay ├──┤ Machine_Enable ├──( Machine_Enable )──
                   I0.0       Q0.0            Q0.1             Q0.1
                
                Network 4: Fault Detection
                ──┤ Safety_Relay ├──┤/Safety_Feedback ├──( TON_Fault )──
                   Q0.0              I0.5                T1, PT: T#500ms
                
                ──┤ T1.Q ├──( Fault_Indicator )──
                   Timer     Q0.2
                
                Light Curtain Safety Circuit:
                
                Inputs:
                I0.0 - Light Curtain OSSD1 (NO)
                I0.1 - Light Curtain OSSD2 (NO)
                I0.2 - Muting Sensor 1 (NO)
                I0.3 - Muting Sensor 2 (NO)
                I0.4 - Muting Enable (NO)
                
                Network 1: Light Curtain Logic
                ──┤ OSSD1 ├──┤ OSSD2 ├──( Light_Curtain_OK )──
                   I0.0       I0.1       M0.1
                
                Network 2: Muting Logic
                ──┤ Muting_Enable ├──┤ Muting_Sensor1 ├──┤ Muting_Sensor2 ├──( Muting_Active )──
                   I0.4             I0.2              I0.3              M0.2
                
                Network 3: Combined Safety
                ──┤ Light_Curtain_OK ├──( Safety_OK )──
                   M0.1                  M0.3
                ──┤ Muting_Active ├────────┘
                   M0.2
                
                Safety Programming Best Practices:
                
                1. Use Normally Closed (NC) contacts for safety inputs
                2. Implement dual-channel safety where required
                3. Use safety-rated PLCs for critical applications
                4. Test safety circuits regularly
                5. Document all safety functions thoroughly
                6. Follow relevant safety standards (ISO 13849, IEC 62061)
                7. Implement proper fault detection and diagnostics
                8. Use safety-certified components
                
                Safety Circuit Testing:
                
                1. Test each safety input individually
                2. Verify proper response to safety violations
                3. Test reset sequences
                4. Validate fault detection logic
                5. Check for proper fail-safe behavior
                6. Document all test results
                """
            },
            {
                "title": "System Configuration",
                "keywords": ["configuration", "hardware config", "cpu parameters", "io modules", "rack", "slot"],
                "content": """
                Hardware configuration and system setup for Siemens PLCs.
                
                Configuration Steps:
                1. Create new project in TIA Portal
                2. Add CPU to rack
                3. Configure CPU parameters (IP address, cycle time, etc.)
                4. Add I/O modules to slots
                5. Assign I/O addresses
                6. Configure communication interfaces
                7. Download configuration to PLC
                
                CPU Parameters:
                - Startup behavior (warm restart, cold restart)
                - Cycle time monitoring
                - Clock settings and time synchronization
                - Web server configuration
                - Communication settings
                
                I/O Configuration:
                - Digital input/output modules
                - Analog input/output modules
                - High-speed counter modules
                - Communication modules
                - Address assignment and diagnostics
                
                Best Practices:
                - Use consistent naming conventions
                - Document all configuration changes
                - Backup configuration regularly
                - Test configuration before commissioning
                """
            }
        ]
    
    def search_knowledge(self, query: str) -> List[Dict[str, Any]]:
        """Search the knowledge base for relevant information"""
        query_lower = query.lower()
        results = []
        
        for item in self.knowledge_base:
            score = 0
            
            # Check title match
            if any(keyword in query_lower for keyword in item["keywords"]):
                score += 10
            
            # Check content match
            content_lower = item["content"].lower()
            query_words = query_lower.split()
            
            for word in query_words:
                if len(word) > 2:  # Skip very short words
                    if word in content_lower:
                        score += content_lower.count(word)
            
            if score > 0:
                results.append({
                    "title": item["title"],
                    "content": item["content"],
                    "score": score,
                    "keywords": item["keywords"]
                })
        
        # Sort by relevance score
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:3]  # Return top 3 results
    
    def ask_question(self, question: str) -> Dict[str, Any]:
        """Answer a question based on the knowledge base"""
        if not question.strip():
            return {
                "question": question,
                "answer": "Please provide a question about Siemens PLCs.",
                "sources": [],
                "num_sources": 0
            }
        
        # Search for relevant information
        results = self.search_knowledge(question)
        
        if not results:
            return {
                "question": question,
                "answer": "I couldn't find specific information about that topic in my knowledge base. Please try rephrasing your question or ask about Siemens S7-1200, S7-1500, TIA Portal, PROFINET, or safety functions.",
                "sources": [],
                "num_sources": 0
            }
        
        # Combine information from top results
        answer_parts = []
        sources = []
        
        for i, result in enumerate(results):
            if i == 0:  # Main answer from best match
                # Extract most relevant section
                content_lines = result["content"].strip().split('\n')
                relevant_lines = []
                
                query_words = question.lower().split()
                for line in content_lines:
                    line_lower = line.lower()
                    if any(word in line_lower for word in query_words if len(word) > 2):
                        relevant_lines.append(line.strip())
                
                if relevant_lines:
                    answer_parts.append('\n'.join(relevant_lines[:5]))  # Top 5 relevant lines
                else:
                    # Fallback to first few lines
                    answer_parts.append('\n'.join(content_lines[:5]))
            
            # Add to sources
            sources.append({
                "content": result["content"][:300] + "..." if len(result["content"]) > 300 else result["content"],
                "metadata": {
                    "title": result["title"],
                    "source": "knowledge_base",
                    "score": result["score"]
                }
            })
        
        answer = '\n\n'.join(answer_parts) if answer_parts else results[0]["content"]
        
        return {
            "question": question,
            "answer": answer,
            "sources": sources,
            "num_sources": len(sources)
        }

def main():
    """Simple command-line interface for testing"""
    assistant = SimplePLCQAAssistant()
    
    print("🔧 Simple Siemens PLC QA Assistant")
    print("=" * 50)
    print("Ask questions about Siemens PLCs, TIA Portal, PROFINET, etc.")
    print("Type 'quit' to exit\n")
    
    while True:
        try:
            question = input("❓ Your question: ").strip()
            
            if question.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not question:
                continue
            
            result = assistant.ask_question(question)
            
            print(f"\n📋 Answer:")
            print("-" * 40)
            print(result["answer"])
            print("-" * 40)
            
            if result["sources"]:
                print(f"\n📚 Sources ({result['num_sources']} found):")
                for i, source in enumerate(result["sources"], 1):
                    print(f"\n{i}. {source['metadata']['title']}")
                    print(f"   Score: {source['metadata'].get('score', 'N/A')}")
            
            print("\n" + "=" * 50)
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
