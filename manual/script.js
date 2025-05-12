// Configuration - Change this URL to match your TabSense Dashboard URL
// This variable can be easily updated to point to your actual TabSense Dashboard
const TABSENSE_DASHBOARD_URL = "http://localhost:8000";

// DOM elements
document.addEventListener("DOMContentLoaded", function() {
    // Update dashboard URL
    const dashboardUrlElement = document.getElementById("dashboard-url");
    dashboardUrlElement.textContent = TABSENSE_DASHBOARD_URL;
    dashboardUrlElement.href = TABSENSE_DASHBOARD_URL;
    
    // Sidebar toggle
    const sidebarToggle = document.getElementById("sidebar-toggle");
    const sidebar = document.querySelector(".sidebar");
    const mainContent = document.querySelector(".main-content");
    
    // Create a visible toggle button for collapsed sidebar
    const collapsedSidebarToggle = document.createElement("button");
    collapsedSidebarToggle.className = "collapsed-sidebar-toggle";
    collapsedSidebarToggle.innerHTML = '<i class="fas fa-bars"></i>';
    document.body.appendChild(collapsedSidebarToggle);
    
    // Toggle sidebar collapse with the sidebar button
    sidebarToggle.addEventListener("click", function() {
        sidebar.classList.toggle("collapsed");
        mainContent.classList.toggle("expanded");
    });
    
    // Toggle sidebar expansion with the collapsed button
    collapsedSidebarToggle.addEventListener("click", function() {
        sidebar.classList.remove("collapsed");
        mainContent.classList.remove("expanded");
    });
    
    // Section collapsing
    const sectionHeadings = document.querySelectorAll(".content-section h2");
    
    sectionHeadings.forEach(heading => {
        heading.addEventListener("click", function() {
            const content = this.nextElementSibling;
            this.classList.toggle("collapsed");
            content.classList.toggle("collapsed");
        });
    });
    
    // Smooth scrolling for anchor links
    const tocLinks = document.querySelectorAll(".toc-link");
    
    tocLinks.forEach(link => {
        link.addEventListener("click", function(e) {
            e.preventDefault();
            
            // Remove active class from all links
            tocLinks.forEach(l => l.classList.remove("active"));
            
            // Add active class to clicked link
            this.classList.add("active");
            
            const targetId = this.getAttribute("href").substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                // If on mobile, close the sidebar
                if (window.innerWidth <= 768) {
                    sidebar.classList.remove("visible");
                }
                
                // Smooth scroll to target
                window.scrollTo({
                    top: targetElement.offsetTop - 20,
                    behavior: "smooth"
                });
                
                // Make sure the section is expanded
                const section = targetElement.closest(".content-section");
                if (section) {
                    const heading = section.querySelector("h2");
                    const content = section.querySelector(".expandable-content");
                    
                    if (heading.classList.contains("collapsed")) {
                        heading.classList.remove("collapsed");
                        content.classList.remove("collapsed");
                    }
                }
            }
        });
    });
    
    // Handle mobile menu
    if (window.innerWidth <= 768) {
        // Create mobile menu toggle button
        const mobileMenuToggle = document.createElement("button");
        mobileMenuToggle.classList.add("mobile-menu-toggle");
        mobileMenuToggle.innerHTML = '<i class="fas fa-bars"></i>';
        document.body.appendChild(mobileMenuToggle);
        
        mobileMenuToggle.addEventListener("click", function() {
            sidebar.classList.toggle("visible");
        });
        
        // Close sidebar when clicking outside
        document.addEventListener("click", function(e) {
            if (!sidebar.contains(e.target) && e.target !== mobileMenuToggle) {
                sidebar.classList.remove("visible");
            }
        });
    }
    
    // Highlight active section on scroll
    const contentSections = document.querySelectorAll(".content-section");
    
    window.addEventListener("scroll", function() {
        let currentSection = "";
        
        contentSections.forEach(section => {
            const sectionTop = section.offsetTop;
            if (window.scrollY >= sectionTop - 100) {
                currentSection = section.getAttribute("id");
            }
        });
        
        tocLinks.forEach(link => {
            link.classList.remove("active");
            const href = link.getAttribute("href").substring(1);
            
            if (href === currentSection) {
                link.classList.add("active");
            }
        });
    });
    
    // Initialize sections - expand first section, collapse others
    if (sectionHeadings.length > 0) {
        sectionHeadings.forEach((heading, index) => {
            if (index !== 0) {
                heading.classList.add("collapsed");
                heading.nextElementSibling.classList.add("collapsed");
            }
        });
    }
    
    // Add animation classes for elements as they scroll into view
    const animateOnScroll = function() {
        const elements = document.querySelectorAll(".subsection");
        
        elements.forEach(element => {
            const position = element.getBoundingClientRect();
            
            // If element is in viewport
            if (position.top < window.innerHeight && position.bottom >= 0) {
                element.style.opacity = "1";
                element.style.transform = "translateY(0)";
            }
        });
    };
    
    // Set initial styles for animation
    const subsections = document.querySelectorAll(".subsection");
    subsections.forEach(element => {
        element.style.opacity = "0";
        element.style.transform = "translateY(20px)";
        element.style.transition = "opacity 0.5s ease, transform 0.5s ease";
    });
    
    // Run animation on load and scroll
    window.addEventListener("load", animateOnScroll);
    window.addEventListener("scroll", animateOnScroll);
});
