# ---------------- OOP Classes ----------------
class Portfolio:
    def __init__(self, name, role, skills, projects, contact):
        self.name = name
        self.role = role
        self.skills = skills        # list of skills
        self.projects = projects    # list of dicts: {'title':..., 'desc':...}
        self.contact = contact      # dict: {'email':..., 'linkedin':...}

class PageGenerator:
    def __init__(self, portfolio):
        self.portfolio = portfolio

    def generate_html(self):
        # Generate dynamic HTML content
        skills_html = ''.join(f"<span>{skill}</span>" for skill in self.portfolio.skills)
        projects_html = ''.join(
            f"<div class='project'><h3>{p['title']}</h3><p>{p['desc']}</p></div>"
            for p in self.portfolio.projects
        )

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.portfolio.name} - Portfolio</title>
    <style>
        body {{ 
            font-family: Arial, sans-serif; 
            margin: 0; 
            padding: 0; 
            background: #F9F9F9; /* Off-white */ 
        }}
        header {{ 
            background: #2F4F4F; /* Deep Green */ 
            color: white; 
            padding: 50px 0; 
            text-align: center; 
        }}
        section {{ 
            padding: 30px 20px; 
            max-width: 900px; 
            margin: auto; 
        }}
        h2 {{ 
            color: #276678; /* Dark Teal */ 
        }}
        .skills span {{ 
            background: #4CA1A3; /* Teal / Blue */ 
            color: white; 
            padding: 5px 12px; 
            margin: 5px; 
            display: inline-block; 
            border-radius: 5px; 
        }}
        .project {{ 
            background: #E5E5E5; /* Soft Gray */ 
            padding: 20px; 
            margin: 15px 0; 
            border-radius: 8px; 
            box-shadow: 0 2px 5px rgba(0,0,0,0.1); 
        }}
        a {{ 
            color: #276678; 
            text-decoration: none; 
        }}
        a:hover {{ 
            text-decoration: underline; 
        }}
    </style>
</head>
<body>
    <header>
        <h1>{self.portfolio.name}</h1>
        <p>{self.portfolio.role}</p>
    </header>

    <section>
        <h2>Skills</h2>
        <div class="skills">{skills_html}</div>
    </section>

    <section>
        <h2>Projects</h2>
        {projects_html}
    </section>

    <section>
        <h2>Contact</h2>
        <p>Email: <a href="mailto:{self.portfolio.contact['email']}">{self.portfolio.contact['email']}</a></p>
        <p>LinkedIn: <a href="{self.portfolio.contact['linkedin']}" target="_blank">{self.portfolio.contact['linkedin']}</a></p>
    </section>
</body>
</html>"""

        # Save HTML file
        with open("portfolio.html", "w") as f:
            f.write(html)
        print("✅ Portfolio landing page generated: portfolio.html")


# ---------------- Initialize Portfolio ----------------
my_portfolio = Portfolio(
    name="Sowmiya",
    role="Python & Web Developer",
    skills=["Python", "HTML", "CSS", "SQL", "OOP"],
    projects=[
        {"title":"Student Management System", "desc":"Python + SQLite + HTML project."},
        {"title":"Landing Page Generator", "desc":"Generates a dynamic portfolio landing page."}
    ],
    contact={
        "email":"sowmiyaofficial1131@gmail.com",
        "linkedin":"https://www.linkedin.com/in/sowmiya-shivan/"
    }
)

# ---------------- Generate HTML ----------------
PageGenerator(my_portfolio).generate_html()
