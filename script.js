document.addEventListener('DOMContentLoaded', function() {

    const form = document.getElementById('application-form');

    if (form) {
        console.log("SUCCESS: application-form found. Attaching event listener."); // <-- DEBUG LINE 1

        form.addEventListener('submit', async function(e) {
            // This is the most important line. It stops the page from reloading.
            e.preventDefault();
            console.log("SUCCESS: Form submitted, preventDefault() was called."); // <-- DEBUG LINE 2

            const submitBtn = form.querySelector('button[type="submit"]');
            const spinner = document.getElementById('spinner');
            const submitText = document.getElementById('submit-text');

            let messageBox = form.querySelector('.message-box');
            if (!messageBox) {
                messageBox = document.createElement('div');
                messageBox.className = 'message-box';
                messageBox.style.cssText = 'padding: 12px 16px; border-radius: 8px; margin-bottom: 16px; text-align: center; font-weight: 500;';
                form.insertBefore(messageBox, submitBtn);
            }

            messageBox.textContent = '';
            submitText.textContent = 'Processing...';
            spinner.classList.remove('hidden');
            submitBtn.disabled = true;

            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());

            try {
                const response = await fetch('/sendmail', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data),
                });
                const responseData = await response.json();

                if (response.ok) {
                    messageBox.textContent = '✅ ' + responseData.message;
                    messageBox.style.color = '#16a34a';
                    messageBox.style.backgroundColor = '#dcfce7';
                    form.reset();
                    
                    // This is the redirect command
                    setTimeout(() => {
                        window.location.href = responseData.redirect || '/thank_you.html';
                    }, 1500);

                } else {
                    messageBox.textContent = '❌ ' + responseData.message;
                    messageBox.style.color = '#dc2626';
                    messageBox.style.backgroundColor = '#fee2e2';
                }
            } catch (error) {
                console.error('Submission Error:', error);
                messageBox.textContent = '❌ Network error. Please check your connection.';
                messageBox.style.color = '#dc2626';
                messageBox.style.backgroundColor = '#fee2e2';
            } finally {
                spinner.classList.add('hidden');
                submitText.textContent = 'Submit Application';
                submitBtn.disabled = false;
            }
        });
    } else {
        console.error("ERROR: Could not find form with ID 'application-form'.");
    }
});