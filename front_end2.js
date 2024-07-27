
async function fetchOrders() {
    try {
        const response = await fetch( 'http://127.0.0.1:5000/fetch_orders');
        console.log('Idhar tak aya maa');
        const orders = await response.json();
        console.log(orders);
        displayOrders(orders);
    } catch (error) {
        console.error('Error fetching orders:', error);
    }
}

function displayOrders(orders) {
    console.log('Entered display orders', orders);
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
            <p>Discount Applied: £${parseFloat(order.discount_applied).toFixed(2)}</p>
            <p>Total Discount: £${parseFloat(order.discount_applied).toFixed(2)}</p>
            <p>Total Price: £${parseFloat(order.final_price).toFixed(2)}</p>
        `;

        orderSummary.appendChild(orderDiv);
    });
}

// Fetch orders on page load
document.addEventListener('DOMContentLoaded', fetchOrders);
