import { useState, useEffect, useRef } from 'react';
import './App.css';
import edamame from './images/edamame.webp';
import hamachiNigiri from './images/hamachi-nigiri.png';
import misoSoup from './images/miso-soup.jpg';
import salmonNigiri from './images/salmon-nigiri.jpeg';
import spicyTemaki from './images/spicy-temaki.webp';
import mochiAssorted from './images/mochi-assorted.jpg';

const MENU = [
  { id: 'edamame', name: 'Edamame', price: 5, image: edamame },
  { id: 'hamachi-nigiri', name: 'Hamachi Nigiri', price: 8, image: hamachiNigiri },
  { id: 'miso-soup', name: 'Miso Soup', price: 4, image: misoSoup },
  { id: 'salmon-nigiri', name: 'Salmon Nigiri', price: 8, image: salmonNigiri },
  { id: 'spicy-temaki', name: 'Spicy Temaki', price: 9, image: spicyTemaki },
  { id: 'mochi-assorted', name: 'Mochi Assorted', price: 7, image: mochiAssorted },
];

function App() {
  const [quantities, setQuantities] = useState({});
  const [status, setStatus] = useState(null);
  const [orderHistory, setOrderHistory] = useState([]);
  const wsRef = useRef(null);

  useEffect(() => {
    fetch('http://localhost:8001/orders/history')
      .then((res) => res.json())
      .then((data) => {
        setOrderHistory(data.map((row) => ({
          items: row.items,
          time: new Date(row.created_at).toLocaleTimeString(),
        })));
      });
  }, []);

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8001/ws');
    wsRef.current = ws;

    ws.onmessage = (event) => {
      const order = JSON.parse(event.data);
      setOrderHistory((prev) => [{ ...order, time: new Date().toLocaleTimeString() }, ...prev]);
    };

    return () => ws.close();
  }, []);

  const updateQuantity = (id, delta) => {
    setQuantities((prev) => ({
      ...prev,
      [id]: Math.max(0, (prev[id] || 0) + delta),
    }));
  };

  const submitOrder = async () => {
    const items = MENU
      .filter((item) => quantities[item.id] > 0)
      .map((item) => ({ item: item.name, quantity: quantities[item.id] }));

    if (items.length === 0) return;

    const response = await fetch('http://localhost:8000/orders', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ items }),
    });
    const data = await response.json();
    setStatus(data.status);
    setQuantities({});
  };

  const total = MENU.reduce(
    (sum, item) => sum + (quantities[item.id] || 0) * item.price,
    0
  );

  return (
    <div className="container">
      <h1 className="title">Sushi Order</h1>
      <div className="menu">
        {MENU.map((item) => (
          <div key={item.id} className="card">
            <img src={item.image} alt={item.name} className="card-image" />
            <div className="card-body">
              <h2 className="card-name">{item.name}</h2>
              <p className="card-price">${item.price}</p>
              <div className="quantity-control">
                <button onClick={() => updateQuantity(item.id, -1)}>-</button>
                <span>{quantities[item.id] || 0}</span>
                <button onClick={() => updateQuantity(item.id, 1)}>+</button>
              </div>
            </div>
          </div>
        ))}
      </div>
      <div className="footer">
        <p className="total">Total: ${total}</p>
        <button className="order-btn" onClick={submitOrder}>
          Place Order
        </button>
        {status && <p className="status">{status}</p>}
      </div>

      <div className="history">
        <h2 className="history-title">Order History</h2>
        {orderHistory.length === 0 ? (
          <p className="history-empty">No orders yet</p>
        ) : (
          orderHistory.map((order, i) => (
            <div key={i} className="history-item">
              <span className="history-time">{order.time}</span>
              <div className="history-items">
                {order.items
                  ? order.items.map((it, j) => (
                      <span key={j}>{it.item} x{it.quantity}</span>
                    ))
                  : <span>{JSON.stringify(order)}</span>
                }
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default App;
