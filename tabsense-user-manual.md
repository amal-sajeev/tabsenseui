<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TabSense Dashboard Manual</title>
    <style>
        /* Dark mode aesthetics inspired by Streamlit */
        :root {
            --primary-bg: #0e1117;
            --secondary-bg: #131921;
            --accent-color: #ff4b4b;
            --text-color: #e5e5e5;
            --subtext-color: #8f9296;
            --border-radius: 0.5rem;
            --transition: all 0.3s ease;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; transition: var(--transition); }
        body { font-family: Arial, sans-serif; background: var(--primary-bg); color: var(--text-color); line-height: 1.6; padding: 2rem; }
        header { text-align: center; margin-bottom: 2rem; }
        header h1 { font-size: 2.5rem; }
        nav { position: fixed; top: 0; left: 0; width: 240px; height: 100%; background: var(--secondary-bg); padding: 2rem 1rem; overflow-y: auto; }
        nav a { display: block; color: var(--text-color); text-decoration: none; padding: 0.5rem 1rem; border-radius: var(--border-radius); margin-bottom: 0.5rem; }
        nav a:hover { background: rgba(255,255,255,0.1); }
        main { margin-left: 260px; }
        section { margin-bottom: 3rem; }
        h2 { font-size: 1.75rem; margin-bottom: 1rem; }
        h3 { font-size: 1.25rem; margin-bottom: 0.75rem; color: var(--accent-color); }
        p { margin-bottom: 1rem; color: var(--subtext-color); }
        ul { list-style: none; margin-left: 1rem; }
        ul li { margin-bottom: 0.5rem; }
        .card { background: var(--secondary-bg); border-radius: var(--border-radius); padding: 1rem; margin-bottom: 1rem; box-shadow: 0 2px 4px rgba(0,0,0,0.5); }
        .toggle-btn { cursor: pointer; position: fixed; bottom: 2rem; right: 2rem; background: var(--accent-color); color: #fff; border: none; padding: 1rem; border-radius: 50%; font-size: 1.5rem; box-shadow: 0 2px 6px rgba(0,0,0,0.5); }
        .fade-enter { opacity: 0; transform: translateY(10px); }
        .fade-enter-active { opacity: 1; transform: translateY(0); }
        .fade-exit { opacity: 1; }
        .fade-exit-active { opacity: 0; }
    </style>
</head>
<body>
    <script>
        // Easily update site link
        const SITE_LINK = "https://your-tabsense-site.com";
    </script>
    <nav>
        <h2>Contents</h2>
        <a href="#introduction">Introduction</a>
        <a href="#getting-started">Getting Started</a>
        <a href="#home-dashboard">Home Dashboard</a>
        <a href="#detection">Detection</a>
        <a href="#schedule-management">Schedule Management</a>
        <a href="#camera-management">Camera Management</a>
        <a href="#reports">Reports</a>
        <a href="#scheduler-control">Scheduler Control</a>
        <a href="#troubleshooting">Troubleshooting</a>
    </nav>
    <main>
        <header>
            <h1>TabSense Dashboard Manual</h1>
            <p>Dark Mode | Streamlined | Interactive</p>
        </header>
        <section id="introduction" class="card">
            <h2>Introduction</h2>
            <p>Welcome to TabSense, your automated stain detection system. Navigate through live feeds, schedules, and reports with ease.</p>
        </section>
        <section id="getting-started" class="card">
            <h2>Getting Started</h2>
            <h3>Accessing the Dashboard</h3>
            <p>Open your browser and go to <a href="" id="site-link">Visit TabSense</a>.</p>
            <h3>Login</h3>
            <p>Use your credentials to sign in.</p>
        </section>
        <!-- Additional sections follow same pattern -->
    </main>
    <button class="toggle-btn" onclick="document.body.classList.toggle('light')">☀️</button>
    <script>
        // Update site link dynamically
        document.getElementById('site-link').href = SITE_LINK;

        // Simple fade transition for sections on scroll
        const cards = document.querySelectorAll('.card');
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if(entry.isIntersecting) {
                    entry.target.classList.add('fade-enter-active');
                }
            });
        }, { threshold: 0.1 });
        cards.forEach(card => {
            card.classList.add('fade-enter');
            observer.observe(card);
        });
    </script>
</body>
</html>
