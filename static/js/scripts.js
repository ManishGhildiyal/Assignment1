document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/events')
        .then(response => {
            if (!response.ok) throw new Error('Failed to fetch events');
            return response.json();
        })
        .then(data => {
            const container = document.getElementById('events-container');
            if (data.length === 0) {
                container.innerHTML = '<p>No events found.</p>';
                return;
            }
            data.forEach(event => {
                const eventDiv = document.createElement('div');
                eventDiv.className = 'event';
                eventDiv.innerHTML = `
                    <h2>${event.name}</h2>
                    <p><strong>Date:</strong> ${event.date}</p>
                    <p><strong>Description:</strong> ${event.description}</p>
                    <form class="ticket-form" data-url="${event.url}">
                        <input type="email" name="email" placeholder="Enter your email" required>
                        <button type="submit">Get Tickets</button>
                    </form>
                `;
                container.appendChild(eventDiv);
            });

            // Add event listeners to forms
            document.querySelectorAll('.ticket-form').forEach(form => {
                form.addEventListener('submit', function(e) {
                    e.preventDefault();
                    const email = form.querySelector('input[name="email"]').value;
                    const url = form.dataset.url;
                    fetch('/get_tickets', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded',
                        },
                        body: `email=${encodeURIComponent(email)}&url=${encodeURIComponent(url)}`
                    })
                    .then(response => {
                        if (!response.ok) throw new Error('Failed to submit email');
                        return response.json();
                    })
                    .then(data => {
                        alert(data.message);
                        window.location.href = data.url;
                    })
                    .catch(error => {
                        console.error('Error submitting email:', error);
                        alert('Error submitting email. Please try again.');
                    });
                });
            });
        })
        .catch(error => {
            console.error('Error fetching events:', error);
            document.getElementById('events-container').innerHTML = '<p>Error loading events. Please try again later.</p>';
        });
});