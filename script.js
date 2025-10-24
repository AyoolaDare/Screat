document.addEventListener('DOMContentLoaded', function() {
    // ===============================
    // 🌀 Animate elements on scroll
    // ===============================
    const animateOnScroll = () => {
        const elements = document.querySelectorAll('.animate-fade-in');
        elements.forEach((el) => {
            const elementPosition = el.getBoundingClientRect().top;
            const screenPosition = window.innerHeight / 1.3;
            if (elementPosition < screenPosition) {
                el.style.opacity = '1';
                el.style.transform = 'translateY(0)';
            }
        });
    };

    window.addEventListener('scroll', animateOnScroll);
    animateOnScroll(); // Initialize on load


    // ===============================
    // 📩 Form submission handling
    // ===============================
    const form = document.getElementById('application-form');
    if (form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();

            // Spinner + Button state
            const submitBtn = form.querySelector('button[type="submit"]');
            const spinner = document.getElementById('spinner');
            const submitText = document.getElementById('submit-text');
            const messageBox = document.createElement('div');
            messageBox.classList.add('message-box');
            form.appendChild(messageBox);

            submitText.textContent = 'Processing...';
            spinner.classList.remove('hidden');
            submitBtn.disabled = true;

            // ===============================
            // 🧾 Validate required fields
            // ===============================
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;

            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    field.classList.add('border-red-500');
                    isValid = false;
                } else {
                    field.classList.remove('border-red-500');
                }
            });

            if (!isValid) {
                alert('Please fill in all required fields marked with *');
                spinner.classList.add('hidden');
                submitText.textContent = 'Submit Application';
                submitBtn.disabled = false;
                return;
            }

            // ===============================
            // 🔞 Validate age
            // ===============================
            const ageInput = document.getElementById('age');
            if (ageInput && ageInput.value < 18) {
                alert('You must be at least 18 years old to apply');
                ageInput.classList.add('border-red-500');
                spinner.classList.add('hidden');
                submitText.textContent = 'Submit Application';
                submitBtn.disabled = false;
                return;
            } else if (ageInput) {
                ageInput.classList.remove('border-red-500');
            }

            // ===============================
            // 📨 Send to Flask backend
            // ===============================
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());

            try {
                const response = await fetch('http://127.0.0.1:5000/sendmail', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data),
                });

                if (response.ok) {
                    messageBox.textContent = 'Message sent successfully!';
                    messageBox.style.color = 'green';
                    form.reset();

                    setTimeout(() => {
                        window.location.href = 'thank_you.html';
                    }, 1000);
                } else {
                    const error = await response.json();
                    messageBox.textContent = error.message || 'Failed to send message.';
                    messageBox.style.color = 'red';
                }
            } catch (error) {
                console.error('Error:', error);
                messageBox.textContent = 'Network error. Please check your connection.';
                messageBox.style.color = 'red';
            } finally {
                spinner.classList.add('hidden');
                submitText.textContent = 'Submit Application';
                submitBtn.disabled = false;
            }
        });
    }


    // ===============================
    // 🌐 Smooth scrolling for anchors
    // ===============================
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
});
