from flask import Flask, render_template, request, redirect, url_for, session
import replicate

from dotenv import load_dotenv
load_dotenv()  # reads .env

import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

context = """
Cesar Augusto Vargas Santini is a Computer Engineering student at the University of Toronto (Faculty of Applied Science and Engineering), specializing in software systems, artificial intelligence, and embedded computing. Date of graduation october 31 of 2025.

🎓 Academic Background
Cesar has completed a comprehensive range of technical courses in both hardware and software, including:

- Machine Learning (ECE421) – covering supervised and unsupervised learning methods, model evaluation, and optimization.
- Applied Fundamentals of Deep Learning (APS360) – focused on modern deep learning architectures, convolutional and recurrent neural networks.
- Introduction to Artificial Intelligence (CSC384) – emphasizing search algorithms, logic, and reasoning for intelligent systems.
- Operating Systems (ECE344) – learned about process management, synchronization, threads, and memory management.
- Computer Networks (ECE361) – studied packet switching, TCP/IP, routing, and socket programming.
- Algorithms and Data Structures (ECE345) – analyzed algorithmic complexity and implementation efficiency.
- Software Communication and Design (ECE297) – practiced teamwork, modular design, and software documentation.
- Engineering Economics & Entrepreneurship (ECE472) and Accounting & Finance (JRE300) – introduced him to financial and business analysis for engineering projects.
- Fundamentals of Optics and Communication Systems – providing an understanding of signal transmission and physical communication media relevant to optical networking.

He also participated in the PEY Co-op Program, integrating professional and technical learning experiences.

💻 Technical Skills
Cesar has strong technical proficiency in:
- Programming Languages: Python, C, C++, JavaScript, SQL (MySQL, PostgreSQL).
- Frameworks & Tools: Flask, Bootstrap, Qt, Power BI, NumPy, Scikit-Learn, Jinja2, GTK.
- Systems & Hardware: Linux/Unix, Atmel microcontrollers, Arduino, and Raspberry Pi development.
- Concepts: Multi-threading, concurrency, sockets, REST APIs, object-oriented design, and database modeling.
- Soft Skills: Critical and analytical thinking, clear communication, and bilingual fluency in English and Spanish (plus beginner French).

🧩 Selected Projects
- Multi-User Chat Server (C/C++) – implemented a real-time multi-threaded chat system using the Berkeley Sockets API with MySQL for managing users and chat rooms. Demonstrated expertise in network programming and concurrency.
- Cloudant REST API (Flask, Bootstrap) – built a full-stack CRUD web app using IBM Cloudant NoSQL, deployed with Gunicorn on Render, showing skill in backend development and cloud deployment.
- Mapping Software for Homeless Support (University of Toronto design project) – created a GIS-based C/GTK desktop app to help users locate available shelters.
- Barcode Inventory Management System (C++/Qt) – integrated barcode scanning for efficient inventory tracking and user interface design.
- Power BI Dashboard – led a data analysis project visualizing sales performance metrics for a transport company.
- Personal Portfolio Website – built a personal webpage (cesaraugusto00.github.io) to showcase his projects and promote his professional profile.

🧠 Interests & Career Goals
Cesar’s interests bridge software engineering, embedded systems, and artificial intelligence. He enjoys working on projects that combine low-level programming (microcontrollers, OS concepts, networking) with AI-driven applications (machine learning and data analysis).

His long-term goal is to become a Systems Software Engineer who designs efficient, scalable, and intelligent systems—potentially developing software infrastructure, communication systems, or embedded AI for robotics and automation.

💼 Summary for LLM Context
Cesar is a technically versatile engineer who combines solid academic grounding in AI and computer systems with hands-on experience in C/C++, Python, Flask, and embedded devices. His projects show an ability to build from low-level hardware to full web applications, and to integrate AI and data analysis tools effectively.

When asked “Why should we hire Cesar?”, an ideal answer should highlight:
- His engineering discipline and analytical mindset from the University of Toronto.
- His experience building functional, well-structured software systems across different domains.
- His interest in applying AI and systems programming to real-world problems.
- His commitment to continuous learning, adaptability, and bilingual communication.

He loves chocolate. he is low maintenance.
He is a good person.
He is a good engineer.
He is a good programmer.
He is a good designer.
He is a good developer.
He is a good manager.
He is a good leader.
He is a good mentor.
He can work extra time in exchange of a good cup of coffee.
He does not like not having coffee.
He enjoys solving problems.
He is a quick learner.
He is a team player.
He is a good communicator.
He is a good listener.
He is a good problem solver.
He is a good decision maker.
He is a good planner.
He is a good organizer.
He is a good leader.

Certifications:
U.N.A.M. (Autonomous National University of Mexico)
Introduction to the world of negotiations. 
The obstacles and driving negotiations. 
Strategies and skills for negotiations. 
Human and business skills to negotiate. 
Irvine University of California
The art of negotiation 
"""


SYSTEM_PROMPT = (
    "You are a busines person that is helping a a recent graduate to get a job. you are representing Cesar who is a computer engineering. You will talk with possible people that will hire him and you will persuade the people to get cesar the job.")

LLAMA3_PROMPT_TEMPLATE = (
    "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n{system_prompt}"
    "<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{prompt}"
    "<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
)




@app.route('/', methods=['GET', 'POST'])
def index():
    # Initialize messages in session if not present (first visit)
    if 'messages' not in session:
        session['messages'] = []
    
    if request.method == 'POST':
        user_message = request.form.get('message', '').strip()

        
        user_prompt = (
                f"Question: {user_message}\n\n"
                f"Context:\n{context}\n\n"
                "Instructions: Answer concisely and be friendly and professional. Remeber you are representing Cesar and you are trying to get him the job."
            )

        inp = {
                "prompt": user_prompt,                 # <-- your question + RAG context
                "system_prompt": SYSTEM_PROMPT,        # <-- stable “modelfile-like” instruction
                "prompt_template": LLAMA3_PROMPT_TEMPLATE,
                "max_new_tokens": 600,
                "temperature": 0.2,
            }

        output = replicate.run(
            "meta/meta-llama-3-8b-instruct",
            input=inp
        )

        output_text = "".join(output)
        print(output_text)
        if user_message:
            # Add user message
            session['messages'].append({
                'type': 'user',
                'text': user_message
            })
            
            # Add response (echo)
            session['messages'].append({
                'type': 'response',
                'text': output_text
            })
            
            session.modified = True
        
        return redirect(url_for('index'))
    
    return render_template('index.html', messages=session.get('messages', []))

@app.route('/clear', methods=['POST'])
def clear():
    session['messages'] = []
    session.modified = True
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
