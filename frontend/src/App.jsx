import React, { useState, useEffect } from 'react';
import { api } from './api';

function App() {
  const [view, setView] = useState('menu'); // menu, check-in, ordering, management
  const [menu, setMenu] = useState([]);
  const [currentVisit, setCurrentVisit] = useState(null);
  const [currentCustomer, setCurrentCustomer] = useState(null);
  const [order, setOrder] = useState({ order: null, items: [] });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchMenu();
  }, []);

  const fetchMenu = async () => {
    try {
      const data = await api.getMenu();
      setMenu(data);
    } catch (err) {
      console.error("Failed to fetch menu", err);
    }
  };

  const handleCheckIn = async (e) => {
    e.preventDefault();
    setLoading(true);
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());

    try {
      const result = await api.checkIn({
        ...data,
        num_people: parseInt(data.num_people),
        reservation_made: data.reservation_made === 'on'
      });
      setCurrentCustomer(result.customer);
      setCurrentVisit(result.visitation);
      setView('ordering');
      // Fetch existing order for this visit if any
      const existingOrder = await api.getOrderByVisit(result.visitation.visit_id);
      if (!existingOrder.detail) {
        setOrder(existingOrder);
      } else {
        setOrder({ order: null, items: [] });
      }
    } catch (err) {
      alert("Check-in failed");
    } finally {
      setLoading(false);
    }
  };

  const handleAddToOrder = async (itemId) => {
    if (!currentVisit || !currentCustomer) return;

    try {
      await api.addToOrder({
        customer_id: currentCustomer.customer_id,
        visit_id: currentVisit.visit_id,
        items: [{ item_id: itemId, quantity: 1 }]
      });
      const updatedOrder = await api.getOrderByVisit(currentVisit.visit_id);
      setOrder(updatedOrder);
    } catch (err) {
      console.error("Ordering failed", err);
    }
  };

  const handleManagementAction = async (action, data) => {
    try {
      if (action === 'delete') await api.deleteItem(data);
      if (action === 'add') await api.addItem(data);
      if (action === 'update') await api.updateItem(data.item_id, data);
      fetchMenu();
    } catch (err) {
      alert("Action failed");
    }
  };

  return (
    <>
      <nav className="navbar glass">
        <h2 className="text-gradient">LUXE DINE</h2>
        <div className="nav-links">
          <span className={`nav-link ${view === 'menu' ? 'active' : ''}`} onClick={() => setView('menu')}>Menu</span>
          <span className={`nav-link ${view === 'check-in' ? 'active' : ''}`} onClick={() => setView('check-in')}>Check-In</span>
          <span className={`nav-link ${view === 'management' ? 'active' : ''}`} onClick={() => setView('management')}>Owner</span>
        </div>
      </nav>

      <main className="container animate-fade">
        {view === 'menu' && <MenuView menu={menu} />}
        {view === 'check-in' && <CheckInView onCheckIn={handleCheckIn} loading={loading} />}
        {view === 'ordering' && (
          <OrderingView
            menu={menu}
            customer={currentCustomer}
            visit={currentVisit}
            order={order}
            onAdd={handleAddToOrder}
          />
        )}
        {view === 'management' && <ManagementView menu={menu} onAction={handleManagementAction} />}
      </main>
    </>
  );
}

function MenuView({ menu }) {
  const categories = [...new Set(menu.map(i => i.category))];
  return (
    <div>
      <header style={{ marginBottom: '3rem', textAlign: 'center' }}>
        <h1 style={{ fontSize: '3.5rem' }}>Our <span className="text-gradient">Exquisite</span> Menu</h1>
        <p style={{ color: 'var(--text-muted)' }}>Handcrafted culinary delights prepared with precision.</p>
      </header>

      {categories.map(cat => (
        <section key={cat} style={{ marginBottom: '4rem' }}>
          <h2 style={{ marginBottom: '1.5rem', borderBottom: '1px solid #333', paddingBottom: '0.5rem' }}>{cat}</h2>
          <div className="grid grid-3">
            {menu.filter(i => i.category === cat).map(item => (
              <div key={item.item_id} className="card">
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                  <div>
                    <h3 style={{ marginBottom: '0.5rem' }}>{item.item_name}</h3>
                    <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>Freshly prepared {item.category} item.</p>
                  </div>
                  <span style={{ color: 'var(--primary)', fontWeight: '700', fontSize: '1.25rem' }}>₹{item.price_inr}</span>
                </div>
              </div>
            ))}
          </div>
        </section>
      ))}
    </div>
  );
}

function CheckInView({ onCheckIn, loading }) {
  return (
    <div style={{ maxWidth: '600px', margin: '4rem auto' }}>
      <div className="card glass" style={{ padding: '3rem' }}>
        <h1 style={{ marginBottom: '1.5rem', textAlign: 'center' }}>Welcome <span className="text-gradient">Guest</span></h1>
        <form onSubmit={onCheckIn}>
          <div className="form-group">
            <label>Full Name</label>
            <input name="name" required placeholder="John Doe" />
          </div>
          <div className="form-group">
            <label>Phone Number</label>
            <input name="phone" required placeholder="+91 99999 88888" />
          </div>
          <div className="grid grid-2">
            <div className="form-group">
              <label>Email</label>
              <input name="email" type="email" placeholder="john@example.com" />
            </div>
            <div className="form-group">
              <label>City</label>
              <input name="city" placeholder="Panihati" />
            </div>
          </div>
          <div className="grid grid-2">
            <div className="form-group">
              <label>Number of People</label>
              <input name="num_people" type="number" defaultValue="1" min="1" />
            </div>
            <div className="form-group" style={{ display: 'flex', alignItems: 'center', gap: '1rem', height: '100%', paddingTop: '1.5rem' }}>
              <label style={{ margin: 0 }}>Reservation Made?</label>
              <input name="reservation_made" type="checkbox" style={{ width: '2rem' }} />
            </div>
          </div>
          <button type="submit" className="btn btn-primary" style={{ width: '100%', marginTop: '1rem' }} disabled={loading}>
            {loading ? 'Processing...' : 'Check-In Table'}
          </button>
        </form>
      </div>
    </div>
  );
}

function OrderingView({ menu, customer, visit, order, onAdd }) {
  return (
    <div className="grid" style={{ gridTemplateColumns: '1fr 350px', alignItems: 'start' }}>
      <div>
        <h1 style={{ marginBottom: '1rem' }}>Order for <span className="text-gradient">{customer.name}</span></h1>
        <p style={{ color: 'var(--text-muted)', marginBottom: '2rem' }}>Visit ID: #{visit.visit_id} | Table for {visit.num_people}</p>

        <div className="grid grid-2">
          {menu.map(item => (
            <div key={item.item_id} className="card" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <h3>{item.item_name}</h3>
                <p style={{ color: 'var(--primary)' }}>₹{item.price_inr}</p>
              </div>
              <button className="btn btn-outline" onClick={() => onAdd(item.item_id)}>Add</button>
            </div>
          ))}
        </div>
      </div>

      <div className="card glass sticky" style={{ top: '100px' }}>
        <h2 style={{ marginBottom: '1.5rem' }}>Your Table Cart</h2>
        {!order.items.length ? (
          <p style={{ color: 'var(--text-muted)' }}>No items ordered yet.</p>
        ) : (
          <div>
            {order.items.map(oi => {
              const itemInfo = menu.find(i => i.item_id === oi.item_id);
              return (
                <div key={oi.id} style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1rem', paddingBottom: '0.5rem', borderBottom: '1px solid rgba(255,255,255,0.1)' }}>
                  <div>
                    <p style={{ fontWeight: 600 }}>{itemInfo?.item_name || 'Item'}</p>
                    <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Qty: {oi.quantity}</p>
                  </div>
                  <p style={{ fontWeight: 600 }}>₹{(itemInfo?.price_inr || 0) * oi.quantity}</p>
                </div>
              );
            })}
            <div style={{ marginTop: '2rem', paddingTop: '1rem', borderTop: '2px solid var(--primary)', display: 'flex', justifyContent: 'space-between' }}>
              <h3 style={{ color: 'var(--primary)' }}>Total</h3>
              <h3 style={{ color: 'var(--primary)' }}>
                ₹{order.items.reduce((sum, oi) => {
                  const item = menu.find(m => m.item_id === oi.item_id);
                  return sum + ((item?.price_inr || 0) * oi.quantity);
                }, 0)}
              </h3>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

function ManagementView({ menu, onAction }) {
  const [editing, setEditing] = useState(null);

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <h1>Menu <span className="text-gradient">Management</span></h1>
        <button className="btn btn-primary" onClick={() => setEditing({ item_name: '', category: '', price_inr: 0 })}>+ New Item</button>
      </div>

      <div className="card glass">
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ color: 'var(--text-muted)', textAlign: 'left' }}>
              <th style={{ padding: '1rem' }}>Name</th>
              <th style={{ padding: '1rem' }}>Category</th>
              <th style={{ padding: '1rem' }}>Price</th>
              <th style={{ padding: '1rem' }}>Actions</th>
            </tr>
          </thead>
          <tbody>
            {menu.map(item => (
              <tr key={item.item_id} style={{ borderTop: '1px solid rgba(255,255,255,0.05)' }}>
                <td style={{ padding: '1rem' }}>{item.item_name}</td>
                <td style={{ padding: '1rem' }}>{item.category}</td>
                <td style={{ padding: '1rem' }}>₹{item.price_inr}</td>
                <td style={{ padding: '1rem' }}>
                  <button className="btn btn-outline" style={{ padding: '0.25rem 0.75rem', marginRight: '0.5rem' }} onClick={() => setEditing(item)}>Edit</button>
                  <button className="btn btn-outline" style={{ padding: '0.25rem 0.75rem', color: '#ff4444', borderColor: '#ff4444' }} onClick={() => onAction('delete', item.item_id)}>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {editing && (
        <div style={{ position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, background: 'rgba(0,0,0,0.8)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000 }}>
          <div className="card glass" style={{ width: '400px' }}>
            <h2>{editing.item_id ? 'Edit Item' : 'New Item'}</h2>
            <form onSubmit={(e) => {
              e.preventDefault();
              const formData = new FormData(e.target);
              const data = Object.fromEntries(formData.entries());
              onAction(editing.item_id ? 'update' : 'add', { ...editing, item_name: data.name, category: data.category, price_inr: parseInt(data.price) });
              setEditing(null);
            }}>
              <div className="form-group">
                <label>Name</label>
                <input name="name" defaultValue={editing.item_name} required />
              </div>
              <div className="form-group">
                <label>Category</label>
                <input name="category" defaultValue={editing.category} required />
              </div>
              <div className="form-group">
                <label>Price (₹)</label>
                <input name="price" type="number" defaultValue={editing.price_inr} required />
              </div>
              <div className="grid grid-2">
                <button type="submit" className="btn btn-primary">Save</button>
                <button type="button" className="btn btn-outline" onClick={() => setEditing(null)}>Cancel</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
