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

class genReport:
    def __init__(self, filename:str):
        # Create document
        global doc
        doc = SimpleDocTemplate(
            filename,
            pagesize=LETTER,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
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
            spaceAfter=8
        )

        global heading3_small
        heading3_small = ParagraphStyle(
            "Heading3Small",
            parent=styles["Heading3"],
            fontSize=11,
            spaceAfter=6
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
        story.append(Paragraph(f"Severity Score: {severityScore} / 100", body_style))

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
        def left_cell(title, subtitle):
            return [
                Paragraph(title, heading2_small),
                Paragraph(subtitle, heading3_small)
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
                left_cell("CRITICAL SAFETY ADVISORY", "RISK STATUS"),
                right_cell("Priority Actions", priorityActions)
            ],
            [
                left_cell("ASSESSMENT EXPLANATION", "WHAT THIS MEANS"),
                right_cell("Quick Vehicle Check", [
                    "Inspect brakes, lights, tires, and mirrors.",
                    "Check for leaks, visible damage, or warning signs.",
                    "If unsure about safety, do not drive yet.",
                ])
            ],
            [
                left_cell("SPECIFIC RISK FACTORS", "FACTORS IDENTIFIED"),
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

        # Build PDF
        doc.build(story)

        print("Updated PDF generated successfully!")


# ## used to test pdf generation, do not uncomment

# # Instantiate mo lang ung class after mo iimport, then pass mo ung output filename
# # INSTANTIATE THIS CLASS FIRST
# reportGenerator = genReport("report.pdf")

# # then input mo ung values ng eval result with these functions, in any order mo nalang icall basta mabigyan ng values
# # palitan mo lang ung nilagay kong hard coded values with the actual variables na naghohold ng values ng evaluation 
# reportGenerator.setRiskLevel("Low Risk")
# reportGenerator.setClientId("2026-001")
# reportGenerator.setSeverityScore("30.2")

# ## Input mo lang dito list ng input variables, automatic mag lalagay ng label
# reportGenerator.setInputSummary(["34","none","less than 1yr","early morning","motorcycle", "none", "etc"]) 

# reportGenerator.setEvalSummary("current condi...")
# reportGenerator.setRecommendedAction("proceed with...")
# reportGenerator.setRiskDistribution(["87.90%","12.10%","0.00%"]) ## input mo dito list ng tatlong risk distribution percentage ng eval score 

# reportGenerator.setReasonList(["No drinking alcohol", "sheesh"]) ## input mo dito list ng reasons pano nakuha ung evaluation score 

# reportGenerator.setPriorityActions([
#                 "Correct the most serious risk factor first.",
#                 "Do not drive if you are impaired, fatigued, or unfit.",
#                 "Check vehicle roadworthiness before travel.",
#             ])

# ## CALL THIS FUNCTION LAST.
# reportGenerator.generateReport() ## keep mo lang to empty, basta macall mo ung function igegenerate na nya ung pdf,