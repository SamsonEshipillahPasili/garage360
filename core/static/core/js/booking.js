document.addEventListener('DOMContentLoaded', function () {
    setUpCreateQuotationLine();
});


function setUpCreateQuotationLine() {
    document.querySelector('#create-quotation-line-btn').addEventListener('click', async (e) => {
        e.preventDefault();

        const form = document.querySelector('#create-quotation-line-form');
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
                document.querySelector('#create-quotation-line-form-container').innerHTML = html;
                setUpCreateQuotationLine();
            }
        } catch (error) {
            console.error('Error submitting form:', error);
        }
    });
}
