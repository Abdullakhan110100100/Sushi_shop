
async function fetchOrders() {
    try {
        const response = await fetch('/fetch_orders');
        const orders = await response.json();
        displayOrders(orders);
    } catch (error) {
        console.error('Error fetching orders:', error);
    }
}

function displayOrders(orders) {
    const orderSummary = document.getElementById('orderSummary');
    orderSummary.innerHTML = '';

    orders.forEach(order => {
        const orderDiv = document.createElement('div');
        orderDiv.className = 'order';

        let itemsHTML = '';
        order.items.forEach(item => {
            itemsHTML += `<p>Sushi ${item.sushi_type}: ${item.quantity} - £${item.price.toFixed(2)}</p>`;
        });

        orderDiv.innerHTML = `
            <p>Order ID: ${order.order_id}</p>
            <p>Order Date: ${new Date(order.order_date).toLocaleString()}</p>
            ${itemsHTML}
            <p>Discount Applied: £${order.discount_applied.toFixed(2)}</p>
            <p>Total Discount: £${order.discount_applied.toFixed(2)}</p>
            <p>Total Price: £${order.final_price.toFixed(2)}</p>
        `;

        orderSummary.appendChild(orderDiv);
    });
}

// Fetch orders on page load
document.addEventListener('DOMContentLoaded', fetchOrders);
