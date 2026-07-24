import { useNavigate } from "react-router-dom";
import {useEffect, useState} from "react";
import "./StudentDashboard.css";
import axios from 'axios';
    
function StudentDashboard() {
const user = JSON.parse(localStorage.getItem("user"));
const [activeSession, setActiveSession] = useState(null);
const navigate = useNavigate();
const [futureSessions, setFutureSessions] = useState([]);
const [showPreOrderModal, setShowPreOrderModal] = useState(false);
const [cartCount, setCartCount] = useState(0);
   useEffect(() => {


    async function loadDashboard() {

       const response = await axios.get(
    "http://127.0.0.1:5000/orders/dashboard"
);
    setFutureSessions(response.data.future_sessions);
    setActiveSession(response.data.active_session);
    }
   
async function loadCartCount() {
    const response = await axios.get(
    `http://localhost:5000/cart/session/${user.user_id}/${activeSession.session_id}`
);
    total = response.data.reduce((sum, item) => sum + item.quantity,0);
    setCartCount(total);
}

    loadDashboard();
    loadCartCount();

}, []);
function handleOrderNow() {

        if (!activeSession) {
            return;
        }

     navigate(`/order/${activeSession.session_id}`);
};

    
    return (
        <div className='student-dashboard'>
            <div className="dashboard-card">
            <h1>Welcome, {user.name} 👋</h1>
            <p className="meal-active">{activeSession ? `${activeSession.meal_name} is Active` : "No active session"}</p>
            <button className="order-now" disabled={!activeSession} onClick={handleOrderNow}>
                Order Now
            </button>
            <button
    className="pre-order"
    onClick={() => setShowPreOrderModal(true)}
>
    Pre-Order
</button>
{showPreOrderModal && (

    <div className="modal-overlay">
        <div className="modal">
        {futureSessions.map(session => (

           <button key={session.session_id}>

    <p>{session.meal_name}</p>

    <p>
        {session.start_time} - {session.end_time}
    </p>

</button>
        ))}
        <button
    onClick={() => setShowPreOrderModal(false)}
>
    Cancel
</button>

    </div>
    </div>

)}
            <button className='cart'>Cart</button>
            <button className='my-orders'>My Orders</button>
            </div>
        </div>
    );

}
export default StudentDashboard;