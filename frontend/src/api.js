const API_BASE_URL = "http://127.0.0.1:8000";

export const api = {
    // Menu
    getMenu: () => fetch(`${API_BASE_URL}/menu`).then(res => res.json()),
    addItem: (item) => fetch(`${API_BASE_URL}/menu`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(item)
    }).then(res => res.json()),
    updateItem: (id, item) => fetch(`${API_BASE_URL}/menu/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(item)
    }).then(res => res.json()),
    deleteItem: (id) => fetch(`${API_BASE_URL}/menu/${id}`, {
        method: 'DELETE'
    }).then(res => res.json()),

    // Customers
    checkIn: (data) => fetch(`${API_BASE_URL}/customers/check-in`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    }).then(res => res.json()),
    getCustomerByPhone: (phone) => fetch(`${API_BASE_URL}/customers/phone/${phone}`).then(res => res.json()),

    // Orders
    addToOrder: (data) => fetch(`${API_BASE_URL}/orders/add`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    }).then(res => res.json()),
    getOrderByVisit: (visitId) => fetch(`${API_BASE_URL}/orders/visit/${visitId}`).then(res => res.json()),
};
