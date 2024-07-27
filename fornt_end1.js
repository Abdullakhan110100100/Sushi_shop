
function calculateTotal() {
    const sushiAPrice = 3;
    const sushiBPrice = 4;
    const discountThreshold = 20;
    const discountRate = 0.1; // 10% discount

    let sushiAQuantity = parseInt(document.getElementById('sushiA').value);
    let sushiBQuantity = parseInt(document.getElementById('sushiB').value);

    let totalBeforeDiscount = (sushiAQuantity * sushiAPrice) + (sushiBQuantity * sushiBPrice);
    let totalAfterDiscount = totalBeforeDiscount;

    if (totalBeforeDiscount >= discountThreshold) {
        totalAfterDiscount = totalBeforeDiscount - (totalBeforeDiscount * discountRate);
    }

    document.getElementById('totalBeforeDiscount').innerText = totalBeforeDiscount.toFixed(2);
    document.getElementById('totalAfterDiscount').innerText = totalAfterDiscount.toFixed(2);
}

async function placeOrder() {
    try {
        let sushiAQuantity = parseInt(document.getElementById('sushiA').value);
        let sushiBQuantity = parseInt(document.getElementById('sushiB').value);

        const response = await fetch('http://localhost:5000/add_to_cart', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ sushiA: sushiAQuantity, sushiB: sushiBQuantity })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        if (data.message === 'Order added successfully') {
            alert('Order placed successfully!');
            order_id = data.order_id
            // Redirect to order summary page
            window.location.href = 'C:\\Users\\rebel\\OneDrive\\Desktop\\abdulla\\web dev\\sushi project\\orders.html';
        }
    } catch (error) {
        console.error('Error placing order:', error);
        alert('Failed to place order. Please try again later.');
    }
}
