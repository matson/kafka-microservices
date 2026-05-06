import { useState } from 'react';                                             
  import './App.css';
                                                                                
  function App() {     
    const [item, setItem] = useState('');
    const [quantity, setQuantity] = useState(1);                                
    const [status, setStatus] = useState(null);
                                                                                
    const submitOrder = async () => {                                           
      const response = await fetch('http://localhost:8000/orders', {
        method: 'POST',                                                         
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ item, quantity }),                               
      });
      const data = await response.json();                                       
      setStatus(data.status);
    };

    return (
      <div style={{ padding: '2rem' }}>
        <h1>Order System</h1>                                                   
        <input
          placeholder="Item"                                                    
          value={item} 
          onChange={(e) => setItem(e.target.value)}                             
        />
        <input                                                                  
          type="number"
          value={quantity}
          onChange={(e) => setQuantity(Number(e.target.value))}
        />                                                                      
        <button onClick={submitOrder}>Place Order</button>
        {status && <p>Status: {status}</p>}                                     
      </div>           
    );
  }

  export default App;   
