document.getElementById('payment-form').addEventListener('submit', function (event) {
    event.preventDefault();

    const amount = document.getElementById('amount').value;
    const description = document.getElementById('description').value;

    fetch('/payment', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ amount, description })
    })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            fetchPayments();
        })
        .catch((error) => {
            console.error('Error:', error);
        });
});

function fetchPayments() {
    fetch('/payments')
        .then(response => response.json())
        .then(data => {
            const paymentList = document.getElementById('payment-list');
            paymentList.innerHTML = '';
            data.forEach(payment => {
                const paymentItem = document.createElement('div');
                paymentItem.innerHTML = `Amount: ${payment.amount}, Description: ${payment.description}`;
                paymentList.appendChild(paymentItem);
            });
        });
}

// Fetch payments on page load
fetchPayments();
