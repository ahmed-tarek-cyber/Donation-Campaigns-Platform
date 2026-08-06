function startCountdown(id, startStr, endStr) {
    const display = document.getElementById('countdown' + id);
    const button = document.getElementById('cart-btn' + id);
    const start = new Date(startStr);
    const end = new Date(endStr);

    function update() {
        const now = new Date();
        if (now < start) {
            const diff = start - now;
            const mins = Math.floor(diff / 60000);
            const secs = Math.floor((diff % 60000) / 1000);
            display.textContent = `Starts in: ${mins}:${secs < 10 ? '0' : ''}${secs}`;
            display.style.color = 'blue';
            if (button) {
                button.textContent = 'Not Started';
                button.disabled = true;
            }
        } else if (now > end) {
            display.textContent = 'Time Left: 00:00';
            display.style.color = 'red';
            if (button) {
                button.textContent = 'Campaign Ended';
                button.disabled = true;
            }
        } else {
            const diff = end - now;
            const mins = Math.floor(diff / 60000);
            const secs = Math.floor((diff % 60000) / 1000);
            display.textContent = `Time Left: ${mins}:${secs < 10 ? '0' : ''}${secs}`;
            display.style.color = 'green';
            if (button) {
                button.textContent = 'Add to Cart';
                button.disabled = false;
            }
        }
    }

    update();
    setInterval(update, 1000);
}

function initCountdowns() {
    document.querySelectorAll('.countdown-box').forEach(box => {
        const id = box.dataset.id;
        const start = box.dataset.start;
        const end = box.dataset.end;
        startCountdown(id, start, end);
    });
}

document.addEventListener('DOMContentLoaded', initCountdowns);
