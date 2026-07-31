
document.addEventListener('DOMContentLoaded', function () {
    setUpCreateUserProfile();
});


function setUpCreateUserProfile() {
    document.querySelector('#create-client-btn').addEventListener('click', async (e) => {
        e.preventDefault();

        const form = document.querySelector('#create-profile-form');
        const formData = new FormData(form);

        try {
            const response = await fetch(form.action, {
                method: 'POST',
                body: formData,
            });

            if (response.redirected) {
                window.location.href = response.url;
            } else {
                const html = await response.text();
                document.querySelector('#create-profile-form-container').innerHTML = html;
                setUpCreateUserProfile();
            }
        } catch (error) {
            console.error('Error submitting form:', error);
        }
    });
}
