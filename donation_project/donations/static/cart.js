 
document.addEventListener("DOMContentLoaded", function () {
    const inputs = Array.from(document.querySelectorAll(".amount-input"));
    const totalSpan = document.getElementById("total");

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function updateTotal() {
        let total = 0;
        inputs.forEach(input => {
            const v = input.value;
            if (!v) return;
            const n = parseFloat(v);
            if (!isNaN(n)) total += n;
        });
        totalSpan.textContent = total.toFixed(2);
    }

     
    function saveAmount(itemId, amount) {
        const csrftoken = getCookie('csrftoken');
        fetch(`/update_amount/${itemId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({ amount: amount })
        })
        .then(resp => resp.json())
        .then(data => {
             
             
        })
        .catch(err => {
            console.error('Could not save amount', err);
        });
    }

    // attach listeners
    inputs.forEach(input => {
        input.addEventListener('input', function () {
            updateTotal();
            const itemId = this.dataset.itemId;
            const amount = this.value || '';
             
            saveAmount(itemId, amount);
        });
    });

     
    updateTotal();
});
