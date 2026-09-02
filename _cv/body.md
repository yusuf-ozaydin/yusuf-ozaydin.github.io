<div class="cv-header">
  <p class="cv-headline">Systems engineering student at GW · operations research and human-centered design <span class="pronouns">(he/him)</span></p>
  <p class="cv-contact">Washington, DC · <a href="mailto:yusuf.ozaydin@gwmail.gwu.edu">yusuf.ozaydin@gwmail.gwu.edu</a> · <a target="_blank" rel="noopener noreferrer" href="https://www.linkedin.com/in/yusuf-ozaydin">LinkedIn</a> · <a target="_blank" rel="noopener noreferrer" href="https://github.com/yusuf-ozaydin">GitHub</a> · U.S. Citizen</p>
  <p class="cv-summary">Yusuf Ozaydin studies systems engineering at the George Washington University, minoring in mathematics and computer science and graduating in 2028. His focus is operations research and human-centered design. At UAB he helped model patient flow through an emergency department; at GW he builds Paceometer, a driving app that shows drivers their pace instead of their speed. He is looking for a summer 2027 internship in operations research or data analysis.</p>
</div>

::: {.cv-synced}
Last synced 2 September 2026.
:::

## Education

<div class="cv-entry">
  <div class="cv-head"><span>The George Washington University</span><span class="cv-dates">Expected May 2028</span></div>
  <div class="cv-sub">B.S. Systems Engineering, minors in Mathematics and Computer Science · Washington, DC · GPA 3.71</div>
  <ul>
    <li>Clark Scholarship for Engineering (renewed annually)</li>
    <li>Dean's List every semester since spring 2025</li>
    <li>Relevant coursework: Mathematics of Operations Research, Quantitative Models in Systems Engineering, Quality Control and Acceptance Sampling, Exploratory Data Analysis, Introductory Programming for Analytics, Algorithms and Data Structures, Systems Thinking and Policy Modeling, Ordinary Differential Equations, Augmented and Virtual Reality</li>
  </ul>
</div>

<div class="cv-entry">
  <div class="cv-head"><span>Vrije Universiteit Amsterdam</span><span class="cv-dates">Spring 2026</span></div>
  <div class="cv-sub">GW Engineering Exchange Program · Amsterdam, Netherlands</div>
  <ul>
    <li>30 ECTS, full-time load</li>
    <li>Coursework: Operations Research III, Statistical Data Analysis, Software Design, Finance I, Philosophy of Mind I</li>
  </ul>
</div>


## Experience

<div class="cv-entry">
  <div class="cv-head"><span>George Washington University Fabrication Lab</span><span class="cv-dates">August 2024 - Present</span></div>
  <div class="cv-sub">Lab Technician Assistant · Washington, DC</div>
  <ul>
    <li>Keep the lab's shared equipment running for a campus-wide base of several hundred students and faculty a week: roughly a dozen 3D printers, three laser cutters, a 3D scanner, a vinyl cutter, and large-format printers.</li>
    <li>Diagnose and repair hardware and software faults on the machines, and walk students through fabrication workflows at the point of use.</li>
    <li>Prototype consumer-product parts with the lab director, drafted in Adobe Illustrator and cut on the laser cutter.</li>
  </ul>
</div>

<div class="cv-entry">
  <div class="cv-head"><span>UAB Department of Health Services Administration</span><span class="cv-dates">June - July 2025</span></div>
  <div class="cv-sub">Research Intern · Birmingham, AL</div>
  <ul>
    <li>Worked in Dr. Abdulaziz Ahmed's research group on a federally funded project to predict and simulate emergency-department overcrowding and build decision-support tools for it.</li>
    <li>Preprocessed and harmonized messy healthcare datasets for feature engineering, and prepared and debugged the Python pipeline.</li>
    <li>Helped tune hyperparameters for the machine-learning models and prepared analysis summaries for the group.</li>
  </ul>
</div>


## Projects & Research

<div class="cv-entry">
  <div class="cv-head"><span>Paceometer</span><span class="cv-dates">June 2026 - Present</span></div>
  <div class="cv-sub">Independent research project, GW</div>
  <ul>
    <li>Designing and building a driving app (a progressive web app in HTML, CSS, and JavaScript) that updates in real time and shows pace next to speed. It works against a well-documented bias where drivers overestimate the time they gain by speeding.</li>
    <li>Found that the original percentage-based trip metric inverted at highway speeds, climbing toward 100% and in effect telling drivers to go faster, and replaced it with a seconds-behind-pace calculation from the underlying t = d/v relationship.</li>
    <li>Ran a WCAG AA accessibility audit with Lighthouse and axe-core: fixed contrast failures as low as 1.28:1 against a 3:1 minimum, added screen-reader announcements, labeled inputs, and reduced-motion support, and brought the app to 100/100 in Lighthouse with zero axe violations.</li>
    <li>Wrote the supporting literature review on time-saving bias, speed and crash risk, and dashboard design. The app keeps all GPS processing on the device, and is now in pilot testing.</li>
  </ul>
<div class="project-links">
  <a class="btn btn-sm btn-outline-primary" target="_blank" rel="noopener noreferrer" href="https://yusuf-ozaydin.github.io/paceometer-app/">App</a>
  <a class="btn btn-sm btn-outline-primary" target="_blank" rel="noopener noreferrer" href="https://raw.githack.com/yusuf-ozaydin/paceometer/refs/heads/main/paceometer_review.html">Literature review</a>
  <a class="btn btn-sm btn-outline-primary" target="_blank" rel="noopener noreferrer" href="https://github.com/yusuf-ozaydin/paceometer-app">App code</a>
  <a class="btn btn-sm btn-outline-primary" target="_blank" rel="noopener noreferrer" href="https://github.com/yusuf-ozaydin/paceometer">Review code</a>
</div>
</div>

<div class="cv-entry">
  <div class="cv-head"><span>Music Graph</span><span class="cv-dates">June 2026 - Present</span></div>
  <div class="cv-sub">Personal project</div>
  <ul>
    <li>Building a graph of a 7,990-track personal Spotify library, with songs as nodes and an edge wherever two tracks share an artist, genre, album, or playlist. Designed the Python data pipeline from scratch.</li>
    <li>Built a three-layer lookup for each artist's genres to get around Spotify API rate limits (Spotify top-artist data, then MusicBrainz ISRC lookups, then a rate-limited Spotify fallback), with name-match checks for multi-artist tracks and local JSON caching so re-runs never re-hit the API.</li>
    <li>Early development. Next steps are Leiden community detection, a Gephi layout, and a web explorer other people can point at their own Spotify accounts.</li>
  </ul>
<div class="project-links">
  <a class="btn btn-sm btn-outline-primary" target="_blank" rel="noopener noreferrer" href="https://github.com/yusuf-ozaydin/music_graph">Code</a>
</div>
</div>

<div class="cv-entry">
  <div class="cv-head"><span>Lift Log</span><span class="cv-dates">July 2026 - Present</span></div>
  <div class="cv-sub">Personal project</div>
  <ul>
    <li>Built a workout-tracker progressive web app in TypeScript for a Push/Pull/Legs/Upper/Lower split, for my own training.</li>
    <li>Picking a day copies the last session as a template. Progression prompts appear when the previous session's sets all hit 8+ reps or estimated 1RM improves, and an analytics view charts weight and 1RM trends and flags stalled lifts.</li>
    <li>All data stays in the browser with no account; the build deploys to GitHub Pages on every push.</li>
  </ul>
<div class="project-links">
  <a class="btn btn-sm btn-outline-primary" target="_blank" rel="noopener noreferrer" href="https://yusuf-ozaydin.github.io/lift-log/">App</a>
  <a class="btn btn-sm btn-outline-primary" target="_blank" rel="noopener noreferrer" href="https://github.com/yusuf-ozaydin/lift-log">Code</a>
</div>
</div>

<div class="cv-entry">
  <div class="cv-head"><span>Workout Tracking Application</span><span class="cv-dates">Spring 2026</span></div>
  <div class="cv-sub">Course project, Vrije Universiteit Amsterdam</div>
  <ul>
    <li>Semester-long deliverable for the Software Design course (instructors Justus Bogner and Ivano Malavolta), built in Java by a multinational student team.</li>
    <li>Wrote the logic that turns a JSON exercise catalog into a workout plan.</li>
    <li>Followed a formal design process: requirements specification, design patterns, and iterative review.</li>
  </ul>
</div>


## Skills

<p><strong>Programming:</strong> Java, Python (pandas, NumPy, Matplotlib), R (proficient); C, JavaScript, HTML/CSS (familiar)</p>
<p><strong>Tools:</strong> Git/GitHub, Quarto, Playwright, Excel, Adobe Illustrator and Photoshop, RobotC</p>
<p><strong>Methods:</strong> Operations research and optimization, graph theory, statistical modeling, software design principles, human-centered design, WCAG accessibility</p>
<p><strong>Learning:</strong> SQL and databases (LinkedIn Learning: SQL Essential Training), Gurobi, LaTeX, Docker</p>
<p><strong>Spoken languages:</strong> English (native), Turkish (native), French (conversational)</p>

## Leadership & Activities

<div class="cv-entry">
  <div class="cv-head"><span>Theta Tau Professional Engineering Fraternity, Gamma Beta Chapter</span><span class="cv-dates">August 2025 - Present</span></div>
  <div class="cv-sub">Community Service Chair (Fall 2026); Member</div>
  <p>Elected to lead chapter service programming and coordinate volunteer events; take part in workshops on engineering ethics and applied practice.</p>
</div>

<div class="cv-entry">
  <div class="cv-head"><span>VEX Robotics (course project)</span><span class="cv-dates">Fall 2025</span></div>
  <div class="cv-sub">Programmer</div>
  <p>Programmed a maze-navigating robot in RobotC for Fundamentals of Systems Engineering, applying the systems-engineering lifecycle and trade studies as part of a small team.</p>
</div>

<div class="cv-entry">
  <div class="cv-head"><span>Hoover Soccer Club / DC Soccer Club</span><span class="cv-dates">2023 - 2025</span></div>
  <div class="cv-sub">Volunteer Coach</div>
  <p>Coached middle-school players across two cities; designed defensive strategy from opponent analysis and handled parent and league logistics.</p>
</div>


