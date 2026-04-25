from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.platypus import PageBreak

# Document Configuration global instantiation
doc = None
story = None

# Document Styles global instantiation(Ignore and do not change)
styles = None

title_style = None
body_style = None

heading2_small = None
heading3_small = None

# Eval information global instantiation
riskLevel = "riskPlaceHolder"

clientId = "usernamePlaceholder"
severityScore = "severityPlaceholder"

inputSummary = None
inputLabels = ["Driver Age:", "Alcohol Consumption:", "Driving Experience:", "Time of Day:", "Expected Trip Duration:", "Vehicle Type:", "Vehicle Age:",
               "Recent Mechanical Issues:", "Brake Condition:", "Last Vehicle Maintenance:", "Weather Condition:", "Visible Road Issues:", "Road Type:",
               "Traffic Level:", "Road Condition:", "Intersections / Busy Crossings:"]

lowRiskDistribution = "lowRiskDistribution"
mediumRiskDistribution = "mediumRiskDistribution"
highRiskDistribution = "highRiskDistribution"

evalSummary = "evalPlaceholder"
recoAction = "recoPlaceholder"

priorityActions = None

reasonList = None

safetyAdvisories = None
assessmentExplanations = None
specificRiskFactors = None

class genReport:
    def __init__(self, filename:str):
        # Create document
        global doc
        doc = SimpleDocTemplate(
            filename,
            pagesize=LETTER,
            rightMargin=52,
            leftMargin=52,
            topMargin=72,
            bottomMargin=42
        )
        
        self.setStyles()

    # Sets the risk level text ( Low Risk, Medium Risk, etc.)
    def setRiskLevel(self, riskLevelText: str):
        global riskLevel
        riskLevel = riskLevelText

    def setClientId(self, clientIdText: str):
        global clientId
        clientId = clientIdText

    def setSeverityScore(self, severityScoreText: str):
        global severityScore
        severityScore = severityScoreText

    def setRiskDistribution(self, riskValues: list):
        global lowRiskDistribution
        global mediumRiskDistribution
        global highRiskDistribution

        lowRiskDistribution, mediumRiskDistribution, highRiskDistribution = riskValues

    def setEvalSummary(self, evalSummaryText: str):
        global evalSummary
        evalSummary = evalSummaryText

    def setRecommendedAction(self, recoActionText: str):
        global recoAction
        recoAction = recoActionText

    def setInputSummary(self, inputs: list):
        global inputSummary
        inputSummary = inputs

    def setReasonList(self, reasons: list):
        global reasonList
        reasonList = reasons

    def setPriorityActions(self, priorityActs: list):
        global priorityActions
        priorityActions = priorityActs

    def setSafetyAdvisory(self, safetyAdvisoryList: list):
        global safetyAdvisories
        safetyAdvisories = safetyAdvisoryList

    def setAssessmentExplanation(self, assessmentExplanationList: list):
        global assessmentExplanations
        assessmentExplanations = assessmentExplanationList
    
    def setSpecificRiskFactors(self, specificRiskFactorList: list):
        global specificRiskFactors
        specificRiskFactors = specificRiskFactorList

    ## Sets the document styles
    def setStyles(self):
        # Styles
        global styles
        styles = getSampleStyleSheet()

        global title_style
        global body_style
        title_style = styles["Title"]
        body_style = styles["BodyText"]

        # Custom smaller headings
        global heading2_small
        heading2_small = ParagraphStyle(
            "Heading2Small",
            parent=styles["Heading2"],
            fontSize=13,
            spaceAfter=6
        )

        global heading3_small
        heading3_small = ParagraphStyle(
            "Heading3Small",
            parent=styles["Heading3"],
            fontSize=11,
            spaceAfter=4
        )

    ## Generates the pdf report with the formatting
    def generateReport(self):
        # Story container
        global story
        story = []

        # --- Title ---
        story.append(Paragraph("PreDriving Accident Risk\nEvaluation and Advisory Report Form", title_style))
        story.append(Spacer(1, 0.25 * inch))

        # --- Eval Result ---
        story.append(Paragraph("Evaluation Result", heading2_small))
        story.append(Spacer(1, 0.05 * inch))

        # --- Risk Level ---
        story.append(Paragraph(f"Accident Risk Level:{riskLevel}", heading2_small))
        story.append(Spacer(1, 0.13 * inch))

        story.append(Paragraph(f"Client ID: {clientId}", body_style))
        story.append(Paragraph(f"Evaluation Score: {severityScore}", body_style))

        # --- INPUT SUMMARY ---
        story.append(Paragraph("INPUT SUMMARY", heading3_small))
        story.append(Spacer(1, 0.1 * inch))

        # - Two Column Bullet List -
        """
        inputSummary: list of strings
        mode:
            'split'  -> first half left, second half right
            'zigzag' -> alternate items between columns
        """

        items = [f"{label} {value}" for label, value in zip(inputLabels, inputSummary)]

        if not items:
            return

        mode='split'
        # --- Split logic ---
        if mode == "split":
            mid = (len(items) + 1) // 2  # left gets extra if odd
            left_items = items[:mid]
            right_items = items[mid:]

        elif mode == "zigzag":
            left_items = items[::2]   # even index
            right_items = items[1::2] # odd index

        else:
            raise ValueError("mode must be 'split' or 'zigzag'")

        # --- Build columns ---
        left_list = ListFlowable(
            [ListItem(Paragraph(i, body_style)) for i in left_items],
            bulletType='bullet'
        )

        right_list = ListFlowable(
            [ListItem(Paragraph(i, body_style)) for i in right_items],
            bulletType='bullet'
        )

        two_col_list = Table([[left_list, right_list]], colWidths=[3*inch, 3*inch])
        story.append(two_col_list)
        story.append(Spacer(1, 0.25 * inch))

        # --- RESULTS ---
        story.append(Paragraph("RESULTS", heading3_small))
        story.append(Spacer(1, 0.1 * inch))

        # --- Two Column Layout (Paragraphs + List) ---
        left_column = [
            Paragraph(f"Evaluation Summary: {evalSummary}", body_style),
            Spacer(1, 0.1 * inch),
            Paragraph(f"Recommended Action: {recoAction}", body_style)
        ]

        right_column = ListFlowable([
            ListItem(Paragraph("RISK DISTRIBUTION", heading3_small), bulletText=None),
            ListItem(Paragraph(f"Low Risk: {lowRiskDistribution}", body_style)),
            ListItem(Paragraph(f"Medium Risk: {mediumRiskDistribution}", body_style)),
            ListItem(Paragraph(f"High Risk: {highRiskDistribution}", body_style)),
        ], bulletType='bullet')

        content_table = Table(
            [[left_column,
              
              right_column]],
            colWidths=[3*inch, 3*inch]
        )

        story.append(content_table)
        story.append(Spacer(1, 0.25 * inch))

        # --- Third Heading3 ---
        story.append(Paragraph("REASONS", heading3_small))
        story.append(Spacer(1, 0.1 * inch))


        reasons_list = ListFlowable(
            [ListItem(Paragraph(i, body_style)) for i in reasonList],
            bulletType='bullet'
        )

        story.append(reasons_list)



        # --- Page Break ---
        story.append(PageBreak())

        # --- Page 2 Title ---
        story.append(Paragraph("ADVISORY AND LEGAL GUIDANCE", heading2_small))
        story.append(Spacer(1, 0.1 * inch))

        story.append(Paragraph("Advisory Assessment", heading2_small))
        story.append(Spacer(1, 0.1 * inch))

        # Helper function to build left column cells
        def left_cell(title, subtitle, bulletpoints):
            return [
                Paragraph(title, heading2_small),
                Paragraph(subtitle, heading3_small),
                ListFlowable(
                    [ListItem(Paragraph(i, body_style)) for i in bulletpoints],
                    bulletType='bullet'
                )
            ]

        # Helper function for right column cells
        def right_cell(title, subtitle: list):
            return [
                Paragraph(title, heading2_small),
                ListFlowable(
                    [ListItem(Paragraph(i, body_style)) for i in subtitle],
                    bulletType='bullet'
                )
            ]

        # --- Create 3 rows x 2 columns layout ---
        page2_data = [
            [
                left_cell("CRITICAL SAFETY ADVISORY", "RISK STATUS", safetyAdvisories),
                right_cell("Priority Actions", priorityActions)
            ],
            [
                left_cell("ASSESSMENT EXPLANATION", "WHAT THIS MEANS", assessmentExplanations),
                right_cell("Quick Vehicle Check", [
                    "Inspect brakes, lights, tires, and mirrors.",
                    "Check for leaks, visible damage, or warning signs.",
                    "If unsure about safety, do not drive yet.",
                ])
            ],
            [
                left_cell("SPECIFIC RISK FACTORS", "FACTORS IDENTIFIED", specificRiskFactors),
                right_cell("Safety Reminder", [
                    "Your safety is in your hands.",
                    "Learn to say no when you are not fit to drive.",
                    "Driver must follow the rules and drive responsibly.",
                ])
            ]
        ]

        page2_table = Table(
            page2_data,
            colWidths=[3*inch, 3*inch],
            rowHeights=None
        )

        # Optional styling (spacing/grid for clarity)
        page2_table.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            # Uncomment if you want visible borders for debugging
            # ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ]))

        story.append(page2_table)

        self.generatePage3()
        self.generatePage4()

        # Build PDF
        doc.build(story)

        print("Updated PDF generated successfully!")

    def generatePage3(self):
        global story

        # --- Page Break ---
        story.append(PageBreak())

         # --- Page 3 Title ---
        story.append(Paragraph("ADVISORY AND LEGAL GUIDANCE", heading2_small))
        story.append(Spacer(1, 0.1 * inch))

        story.append(Paragraph("Safety Discipline", heading2_small))
        story.append(Spacer(1, 0.1 * inch))

        data = [
            ['"Pray Before Driving"', '"Your safety is in your hands."', '"Learn to Say NO"'],
            [
                "- Take a moment to center yourself\nspiritually and mentally.\n"
                "- Ask for safe travels and protection\nfor yourself and others on the road."
            ,'"Drivers MUST Follow Rules"', '"Better Late Than Never"']
        ]

        table1 = Table(data)

        story.append(table1)

        story.append(Paragraph("Pre-Drive Health Checklist", heading2_small))
        story.append(Spacer(1, 0.1 * inch))

        # --- Column 1 content ---
        col1 = [
            Paragraph("✓ Get Adequate Sleep", heading2_small),
            Spacer(1, 0.1 * inch),
            Paragraph("Ensure proper sleep before driving.", body_style),
            Spacer(1, 0.08 * inch),
            Paragraph("Aim for 7–8 hours of quality rest.", body_style),
            Spacer(1, 0.08 * inch),
            Paragraph("Never drive when sleepy, fatigued, or unable to focus properly.", body_style),
        ]

        # --- Column 2 content ---
        col2 = [
            Paragraph("✓ Eat Proper Meals", heading2_small),
            Spacer(1, 0.1 * inch),
            Paragraph("Eat before long drives.", body_style),
            Spacer(1, 0.08 * inch),
            Paragraph("Avoid driving on an empty stomach for long trips.", body_style),
        ]

        # --- Column 3 content ---
        col3 = [
            Paragraph("✓ Stay Hydrated", heading2_small),
            Spacer(1, 0.1 * inch),
            Paragraph("Dehydration may cause headache, fatigue, and reduced alertness.", body_style),
            Spacer(1, 0.1 * inch),
            Paragraph("Drink water regularly.", body_style),
        ]

        # --- Column 4 content ---
        col4 = [
            Paragraph("✓ Check Medical Fitness", heading2_small),
            Spacer(1, 0.1 * inch),
            Paragraph("Do not drive if you feel dizzy, ill, emotionally unstable, or affected by drowsy medication.", body_style),
            Spacer(1, 0.1 * inch),
            Paragraph("Impaired means your ability to operate a vehicle safely is reduced.", body_style),
        ]

        # --- Build table ---
        four_col_table = Table(
            [[col1, col2, col3, col4]],
            colWidths=[2*inch, 2*inch, 2*inch]
        )

        four_col_table.setStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ])

        # Add to story
        story.append(four_col_table)
        story.append(Spacer(1, 0.3 * inch))

        # --- Column 1 content ---
        col1 = [
            Paragraph("Discipline Checklist", heading2_small),
            Spacer(1, 0.1 * inch),
            Paragraph("No distracted driving.", body_style),
            Spacer(1, 0.08 * inch),
            Paragraph("No aggressive driving", body_style),
            Spacer(1, 0.08 * inch),
            Paragraph("No driving under influence", body_style),
            Spacer(1, 0.08 * inch),
            Paragraph("Follow traffic signals and road signs", body_style),
            Spacer(1, 0.08 * inch),
            Paragraph("Yield properly and respect pedestrians", body_style),

        ]

        # --- Column 2 content ---
        col2 = [
            Paragraph("Proper Vehicle Checking", heading2_small),
            Spacer(1, 0.1 * inch),
            Paragraph("Walk around the vehicle before every trip.", body_style),
            Spacer(1, 0.08 * inch),
            Paragraph("Check tires, lights, brakes, mirrors, and visible damage.", body_style),
            Spacer(1, 0.08 * inch),
            Paragraph("Confirm the vehicle is roadworthy before departure.", body_style),
        ]

        # --- Column 3 content ---
        col3 = [
            Paragraph("Maximum Continuous Driving", heading2_small),
            Spacer(1, 0.1 * inch),
            Paragraph("Avoid driving continuously beyond 6 hours.", body_style),
            Spacer(1, 0.08 * inch),
            Paragraph("Take breaks every 2–3 hours whenever possible.", body_style),
            Spacer(1, 0.08 * inch),
            Paragraph("Stop earlier if you feel sleepy, tired, dizzy, or unfocused.", body_style),
        ]

        # --- Build table ---
        three_col_table = Table(
            [[col1, col2, col3]],
            colWidths=[2*inch, 2*inch, 2*inch]
        )

        three_col_table.setStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ])

        # Add to story
        story.append(three_col_table)
        story.append(Spacer(1, 0.3 * inch))

    def generatePage4(self):
        global story

        # --- Page Break ---
        story.append(PageBreak())

         # --- Page 3 Title ---
        story.append(Paragraph("ADVISORY AND LEGAL GUIDANCE", heading2_small))
        story.append(Spacer(1, 0.1 * inch))

        story.append(Paragraph("Laws and regulations", heading2_small))
        story.append(Spacer(1, 0.1 * inch))

        # --- Column 1 content ---
        col1 = [
            Paragraph("Legal Liability", heading2_small),
            Spacer(1, 0.1 * inch),
            Paragraph("Drivers may be criminally and civilly liable\nfor accidents caused by negligence or reckless driving.", body_style),
        ]

        # --- Column 2 content ---
        col2 = [
            Paragraph("Insurance Required", heading2_small),
            Spacer(1, 0.1 * inch),
            Paragraph("Required vehicle documents and insurance must be in order before travel.", body_style),
        ]

        # --- Column 3 content ---
        col3 = [
            Paragraph("High Risk Penalties", heading2_small),
            Spacer(1, 0.1 * inch),
            Paragraph("Repeated violations may result in larger fines, suspension, or other serious legal consequences.", body_style),
        ]

        # --- Build table ---
        three_col_table = Table(
            [[col1, col2, col3]],
            colWidths=[2*inch, 2*inch, 2*inch]
        )

        three_col_table.setStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ])

        # Add to story
        story.append(three_col_table)
        story.append(Spacer(1, 0.3 * inch))

        self.generatePage42()
        self.generatePage43()

    def generatePage42(self):
        # --- Column 1 content ---
        col1 = [
            Paragraph("RA 4136", heading2_small),
            Spacer(1, 0.1 * inch),
            Paragraph("- Land Transportation and Traffic Code"),
            Paragraph("- Vehicle registration and licensing rules"),
            Paragraph("- Traffic violations and penalties"),
            Paragraph("- Roadworthiness standards"),
        ]

        # --- Column 2 content ---
        col2 = [
            Paragraph("RA 10913", heading2_small),
            Spacer(1, 0.1 * inch),
            Paragraph("Anti-Distracted Driving Act"),
            Paragraph("No mobile phone use while driving"),
            Paragraph("Hands-free use has limited exceptions"),
            Paragraph("Violations may result in fines"),
            ]

        # --- Column 3 content ---
        col3 = [
            Paragraph("RA 8750", heading2_small),
            Spacer(1, 0.1 * inch),
            Paragraph("Seat Belt Use Act"),
            Paragraph("Promotes occupant safety compliance"),
            Paragraph("Violations may result in fines")
        ]

        # --- Build table ---
        three_col_table = Table(
            [[col1, col2, col3]],
            colWidths=[2*inch, 2*inch, 2*inch]
        )

        three_col_table.setStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ])

        # Add to story
        story.append(three_col_table)
        story.append(Spacer(1, 0.3 * inch))
    
    def generatePage43(self):
        # --- Column 1 content ---
        col1 = [
            Paragraph("LTO Compliance", heading2_small),
            Spacer(1, 0.1 * inch),
            Paragraph("- Valid driver’s license"),
            Paragraph("- Updated vehicle registration"),
            Paragraph("- Required insurance"),
            Paragraph("- Medical fitness to drive"),
        ]

        # --- Column 2 content ---
        col2 = [
            Paragraph("Mandatory Before Driving", heading2_small),
            Spacer(1, 0.1 * inch),
            Paragraph("Valid driver’s license"),
            Paragraph("Updated registration"),
            Paragraph("Required insurance"),
            Paragraph("Fit driver condition"),
            ]

        # --- Column 3 content ---
        col3 = [
            Paragraph("Legal Responsibility", heading2_small),
            Spacer(1, 0.1 * inch),
            Paragraph("Driving requires discipline and accountability."),
            Paragraph("Reckless or negligent behavior may lead to legal consequences."),
            Paragraph("Always make safe and lawful driving decisions.")
        ]

        # --- Build table ---
        three_col_table = Table(
            [[col1, col2, col3]],
            colWidths=[2*inch, 2*inch, 2*inch]
        )

        three_col_table.setStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ])

        # Add to story
        story.append(three_col_table)
        story.append(Spacer(1, 0.3 * inch))

    def setEvaluationScore(self, evaluationScoreText: str):
        global severityScore
        severityScore = evaluationScoreText
        
        