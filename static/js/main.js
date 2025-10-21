document.addEventListener('DOMContentLoaded', function() {
    // Get references to DOM elements
    const form = document.getElementById('job-form');
    const jobDescriptionTextarea = document.getElementById('job_description');
    const resumeTextTextarea = document.getElementById('resume_text');
    const resumeFileInput = document.getElementById('resume_file');
    const resumeMethodRadios = document.querySelectorAll('input[name="resume_method"]');
    const resumeTextSection = document.getElementById('resume-text-section');
    const resumeFileSection = document.getElementById('resume-file-section');
    const fileInfo = document.getElementById('file-info');
    const loadingIndicator = document.getElementById('loading');
    const resumeSuggestionsDiv = document.getElementById('resume-suggestions');
    const coverLetterDiv = document.getElementById('cover-letter');
    const matchScoreEl = document.getElementById('match-score');
    const matchBarEl = document.getElementById('match-bar');
    const matchStrengthsEl = document.getElementById('match-strengths');
    const matchGapsEl = document.getElementById('match-gaps');
    const errorMessage = document.getElementById('error-message');
    const errorText = document.getElementById('error-text');

    // Smooth scrolling for navigation links
    function initSmoothScrolling() {
        const navLinks = document.querySelectorAll('a[href^="#"]');
        navLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                const targetId = this.getAttribute('href');
                const targetSection = document.querySelector(targetId);
                
                if (targetSection) {
                    const offsetTop = targetSection.offsetTop - 80; // Account for fixed nav
                    window.scrollTo({
                        top: offsetTop,
                        behavior: 'smooth'
                    });
                }
            });
        });
    }

    // Scroll reveal animations
    function initScrollReveal() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('revealed');
                }
            });
        }, observerOptions);

        // Observe all scroll-reveal elements
        const revealElements = document.querySelectorAll('.scroll-reveal');
        revealElements.forEach(el => observer.observe(el));
    }

    // Parallax effect for hero section
    function initParallax() {
        window.addEventListener('scroll', () => {
            const scrolled = window.pageYOffset;
            const heroSection = document.getElementById('home');
            if (heroSection) {
                const rate = scrolled * -0.5;
                heroSection.style.transform = `translateY(${rate}px)`;
            }
        });
    }

    // Navbar background on scroll
    function initNavbarScroll() {
        const navbar = document.querySelector('nav');
        window.addEventListener('scroll', () => {
            if (window.scrollY > 80) {
                navbar.classList.add('nav-scrolled');
            } else {
                navbar.classList.remove('nav-scrolled');
            }
        });
    }

    // Initialize all scroll effects
    initSmoothScrolling();
    initScrollReveal();
    initParallax();
    initNavbarScroll();

    // Add typing animation to hero text
    function initTypingAnimation() {
        const heroTitle = document.querySelector('#home h1');
        if (heroTitle) {
            const text = heroTitle.textContent;
            heroTitle.textContent = '';
            let i = 0;
            const typeWriter = () => {
                if (i < text.length) {
                    heroTitle.textContent += text.charAt(i);
                    i++;
                    setTimeout(typeWriter, 50);
                }
            };
            setTimeout(typeWriter, 1000);
        }
    }

    // Add floating animation to feature cards
    function initFloatingCards() {
        const cards = document.querySelectorAll('.hover-lift');
        cards.forEach((card, index) => {
            card.style.animationDelay = `${index * 0.1}s`;
        });
    }

    // Add progress bar animation
    function initProgressAnimation() {
        const progressBars = document.querySelectorAll('.animate-pulse-slow');
        progressBars.forEach((bar, index) => {
            setTimeout(() => {
                bar.style.animation = 'pulse 3s ease-in-out infinite';
            }, index * 200);
        });
    }

    // Initialize animations
    initTypingAnimation();
    initFloatingCards();
    initProgressAnimation();

    // Add submit event listener to the form
    form.addEventListener('submit', async function(event) {
        event.preventDefault(); // Prevent default form submission
        
        // Show loading indicator with animation
        loadingIndicator.classList.remove('hidden');
        loadingIndicator.scrollIntoView({ behavior: 'smooth', block: 'center' });
        errorMessage.classList.add('hidden');
        
        // Clear previous results with fade out
        resumeSuggestionsDiv.style.opacity = '0.5';
        coverLetterDiv.style.opacity = '0.5';
        
        setTimeout(() => {
            resumeSuggestionsDiv.innerHTML = '<p class="text-gray-500 italic text-lg">Your personalized resume suggestions will appear here...</p>';
            coverLetterDiv.innerHTML = '<p class="text-gray-500 italic text-lg">Your personalized cover letter will appear here...</p>';
            resumeSuggestionsDiv.style.opacity = '1';
            coverLetterDiv.style.opacity = '1';
        }, 300);
        
        // Get job description and selected model
        const jobDescription = jobDescriptionTextarea.value.trim();
        const selectedModel = document.querySelector('input[name="ai_model"]:checked').value;
        
        // Validate job description
        if (!jobDescription) {
            showError('Please provide a job description.');
            loadingIndicator.classList.add('hidden');
            return;
        }
        
        // Check which resume method is selected
        const selectedMethod = document.querySelector('input[name="resume_method"]:checked').value;
        
        try {
            let response;
            
            if (selectedMethod === 'file') {
                // Handle file upload
                const resumeFile = resumeFileInput.files[0];
                
                if (!resumeFile) {
                    showError('Please select a resume file.');
                    loadingIndicator.classList.add('hidden');
                    return;
                }
                
                // Validate file type
                const allowedTypes = ['.pdf', '.docx', '.doc', '.txt'];
                const fileExtension = '.' + resumeFile.name.split('.').pop().toLowerCase();
                
                if (!allowedTypes.includes(fileExtension)) {
                    showError('Please upload a PDF, DOCX, DOC, or TXT file.');
                    loadingIndicator.classList.add('hidden');
                    return;
                }
                
                // Create FormData for file upload
                const formData = new FormData();
                formData.append('job_description', jobDescription);
                formData.append('resume_file', resumeFile);
                formData.append('ai_model', selectedModel);
                
                // Make API request with file upload
                response = await fetch('/analyze', {
                    method: 'POST',
                    body: formData
                });
                
            } else {
                // Handle text input
                const resumeText = resumeTextTextarea.value.trim();
                
                if (!resumeText) {
                    showError('Please provide your resume text.');
                    loadingIndicator.classList.add('hidden');
                    return;
                }
                
                // Make API request with JSON
                response = await fetch('/analyze', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        job_description: jobDescription,
                        resume_text: resumeText,
                        ai_model: selectedModel
                    })
                });
            }
            
            // Check if response is ok
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
            }
            
            // Parse JSON response
            const data = await response.json();
            
            // Populate the result divs with animation
            if (data.suggestions) {
                resumeSuggestionsDiv.innerHTML = formatText(data.suggestions);
                resumeSuggestionsDiv.style.transform = 'translateY(20px)';
                resumeSuggestionsDiv.style.opacity = '0';
                setTimeout(() => {
                    resumeSuggestionsDiv.style.transition = 'all 0.6s ease-out';
                    resumeSuggestionsDiv.style.transform = 'translateY(0)';
                    resumeSuggestionsDiv.style.opacity = '1';
                }, 100);
            } else {
                resumeSuggestionsDiv.innerHTML = '<p class="text-gray-500 italic text-lg">No suggestions generated.</p>';
            }
            
            if (data.cover_letter) {
                coverLetterDiv.innerHTML = formatText(data.cover_letter);
                coverLetterDiv.style.transform = 'translateY(20px)';
                coverLetterDiv.style.opacity = '0';
                setTimeout(() => {
                    coverLetterDiv.style.transition = 'all 0.6s ease-out';
                    coverLetterDiv.style.transform = 'translateY(0)';
                    coverLetterDiv.style.opacity = '1';
                }, 200);
            } else {
                coverLetterDiv.innerHTML = '<p class="text-gray-500 italic text-lg">No cover letter generated.</p>';
            }
            
            // Render match insights if available
            if (data.match) {
                const { score, strengths = [], gaps = [] } = data.match;
                if (typeof score === 'number' && matchScoreEl && matchBarEl) {
                    const pct = Math.max(0, Math.min(100, Math.round(score)));
                    matchScoreEl.textContent = pct + '%';
                    matchBarEl.style.width = pct + '%';
                    matchBarEl.classList.toggle('bg-green-500', pct >= 70);
                    matchBarEl.classList.toggle('bg-yellow-500', pct >= 40 && pct < 70);
                    matchBarEl.classList.toggle('bg-red-500', pct < 40);
                }
                if (matchStrengthsEl) {
                    matchStrengthsEl.innerHTML = strengths.length
                        ? strengths.map(s => `<li>${s}</li>`).join('')
                        : '<li class="italic text-gray-500">No clear strengths identified</li>';
                }
                if (matchGapsEl) {
                    matchGapsEl.innerHTML = gaps.length
                        ? gaps.map(g => `<li>${g}</li>`).join('')
                        : '<li class="italic text-gray-500">No major gaps detected</li>';
                }
            }

            // Scroll to results
            setTimeout(() => {
                resumeSuggestionsDiv.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }, 500);
            
        } catch (error) {
            console.error('Error:', error);
            showError(`Failed to analyze your resume: ${error.message}`);
        } finally {
            // Hide loading indicator
            loadingIndicator.classList.add('hidden');
        }
    });
    
    // Function to show error messages
    function showError(message) {
        errorText.textContent = message;
        errorMessage.classList.remove('hidden');
    }
    
    // Function to format text (basic markdown-like formatting)
    function formatText(text) {
        if (!text) return '';
        
        // Convert line breaks to <br> tags
        let formatted = text.replace(/\n/g, '<br>');
        
        // Convert **bold** to <strong>
        formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        
        // Convert *italic* to <em>
        formatted = formatted.replace(/\*(.*?)\*/g, '<em>$1</em>');
        
        // Convert ### headers to <h3>
        formatted = formatted.replace(/### (.*?)(<br>|$)/g, '<h3 class="text-lg font-semibold text-gray-800 mt-4 mb-2">$1</h3>');
        
        // Convert ## headers to <h2>
        formatted = formatted.replace(/## (.*?)(<br>|$)/g, '<h2 class="text-xl font-bold text-gray-800 mt-4 mb-2">$1</h2>');
        
        // Convert # headers to <h1>
        formatted = formatted.replace(/# (.*?)(<br>|$)/g, '<h1 class="text-2xl font-bold text-gray-800 mt-4 mb-2">$1</h1>');
        
        // Convert bullet points (- or *) to <ul><li>
        formatted = formatted.replace(/(?:^|<br>)([-*]) (.*?)(?=<br>[-*]|<br>$|$)/gm, '<ul class="list-disc list-inside mb-2"><li class="ml-4">$2</li></ul>');
        
        // Clean up multiple <br> tags
        formatted = formatted.replace(/(<br>){3,}/g, '<br><br>');
        
        return formatted;
    }
    
    // Handle resume method radio button changes
    resumeMethodRadios.forEach(radio => {
        radio.addEventListener('change', function() {
            if (this.value === 'text') {
                resumeTextSection.classList.remove('hidden');
                resumeFileSection.classList.add('hidden');
                resumeTextTextarea.required = true;
                resumeFileInput.required = false;
            } else {
                resumeTextSection.classList.add('hidden');
                resumeFileSection.classList.remove('hidden');
                resumeTextTextarea.required = false;
                resumeFileInput.required = true;
            }
        });
    });
    
    // Handle file selection
    resumeFileInput.addEventListener('change', function() {
        const file = this.files[0];
        if (file) {
            fileInfo.innerHTML = `
                <div class="flex items-center text-green-600">
                    <svg class="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                    </svg>
                    Selected: ${file.name} (${(file.size / 1024 / 1024).toFixed(2)} MB)
                </div>
            `;
            fileInfo.classList.remove('hidden');
        } else {
            fileInfo.classList.add('hidden');
        }
    });
    
    // Add drag and drop functionality
    const dropZone = resumeFileSection.querySelector('.border-dashed');
    
    dropZone.addEventListener('dragover', function(e) {
        e.preventDefault();
        this.classList.add('border-blue-400', 'bg-blue-50');
    });
    
    dropZone.addEventListener('dragleave', function(e) {
        e.preventDefault();
        this.classList.remove('border-blue-400', 'bg-blue-50');
    });
    
    dropZone.addEventListener('drop', function(e) {
        e.preventDefault();
        this.classList.remove('border-blue-400', 'bg-blue-50');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            const file = files[0];
            const allowedTypes = ['.pdf', '.docx', '.doc', '.txt'];
            const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
            
            if (allowedTypes.includes(fileExtension)) {
                resumeFileInput.files = files;
                resumeFileInput.dispatchEvent(new Event('change'));
            } else {
                showError('Please upload a PDF, DOCX, DOC, or TXT file.');
            }
        }
    });
    
    // Add some helpful placeholder text that appears when textareas are focused
    jobDescriptionTextarea.addEventListener('focus', function() {
        if (this.value === '') {
            this.placeholder = 'Paste the complete job description including requirements, responsibilities, and qualifications...';
        }
        this.parentElement.classList.add('ring-2', 'ring-blue-500');
    });
    
    resumeTextTextarea.addEventListener('focus', function() {
        if (this.value === '') {
            this.placeholder = 'Paste your complete resume including work experience, education, skills, and achievements...';
        }
        this.parentElement.classList.add('ring-2', 'ring-green-500');
    });
    
    // Reset placeholder text when not focused
    jobDescriptionTextarea.addEventListener('blur', function() {
        if (this.value === '') {
            this.placeholder = 'Paste the complete job description including requirements, responsibilities, and qualifications...';
        }
        this.parentElement.classList.remove('ring-2', 'ring-blue-500');
    });
    
    resumeTextTextarea.addEventListener('blur', function() {
        if (this.value === '') {
            this.placeholder = 'Paste your complete resume including work experience, education, skills, and achievements...';
        }
        this.parentElement.classList.remove('ring-2', 'ring-green-500');
    });

    // Add character count for textareas
    function addCharacterCount(textarea, maxLength = 5000) {
        const container = textarea.parentElement;
        const counter = document.createElement('div');
        counter.className = 'text-sm text-gray-500 mt-2 text-right';
        container.appendChild(counter);
        
        function updateCounter() {
            const count = textarea.value.length;
            counter.textContent = `${count}/${maxLength} characters`;
            if (count > maxLength * 0.9) {
                counter.classList.add('text-red-500');
            } else {
                counter.classList.remove('text-red-500');
            }
        }
        
        textarea.addEventListener('input', updateCounter);
        updateCounter();
    }
    
    // Initialize character counters
    addCharacterCount(jobDescriptionTextarea, 10000);
    addCharacterCount(resumeTextTextarea, 15000);

    // Add success animation for form submission
    function showSuccessMessage() {
        const successDiv = document.createElement('div');
        successDiv.className = 'fixed top-20 right-6 bg-green-500 text-white px-6 py-4 rounded-lg shadow-lg z-50 transform translate-x-full transition-transform duration-300';
        successDiv.innerHTML = '<i class="fas fa-check-circle mr-2"></i>Analysis completed successfully!';
        document.body.appendChild(successDiv);
        
        setTimeout(() => {
            successDiv.style.transform = 'translateX(0)';
        }, 100);
        
        setTimeout(() => {
            successDiv.style.transform = 'translateX(100%)';
            setTimeout(() => successDiv.remove(), 300);
        }, 3000);
    }

    // Add keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + Enter to submit form
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            if (form.checkValidity()) {
                form.dispatchEvent(new Event('submit'));
            }
        }
    });
});
