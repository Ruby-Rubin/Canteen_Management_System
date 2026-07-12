import { useLocation } from "react-router-dom";
import {useEffect, useState} from "react";
import "./StudentDashboard.css";
import axios from 'axios';

    
function StudentDashboard() {
const location = useLocation();
const [activeSession, setActiveSession] = useState(null);
const [futureSessions, setFutureSessions] = useState([]);
const user = location.state.user;
   useEffect(() => {

    async function loadDashboard() {

       const response = await axios.get(
    "http://127.0.0.1:5000/orders/dashboard"
);
     setFutureSessions(response.data.future_sessions);
    setActiveSession(response.data.active_session);
    }
   

    loadDashboard();

}, []);

    

    
    return (
        <div className='student-dashboard'>
            <div className="dashboard-card">
            <h1>Welcome, {user.name} 👋</h1>
            <p className="meal-active">{activeSession ? `${activeSession.meal_name} is Active` : "No active session"}</p>
            <button className="order-now">Order Now</button>
            <button className='pre-order'>Pre-Order</button>
            <button className='cart'>Cart</button>
            <button className='my-orders'>My Orders</button>
            </div>
        </div>
    );
}

export default StudentDashboard;