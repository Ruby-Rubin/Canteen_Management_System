import { useLocation } from "react-router-dom";
import {useEffect, useState} from "react";
import "./StudentDashboard.css";
import axios from "axios";

function StudentDashboard() {
    useEffect(() => { const  response=axios.get("http:///orders/preorders")

}, []);


    const location = useLocation();
    const [activeSession, setActiveSession] = useState(null);
    const user = location.state.user;

    
    return (
        <div className='student-dashboard'>
            <div className="dashboard-card">
            <h1>Welcome, {user.name} 👋</h1>
            <p className="meal-active">{activeSession}</p>
            <button className="order-now">Order Now</button>
            <button className='pre-order'>Pre-Order</button>
            <button className='cart'>Cart</button>
            <button className='my-orders'>My Orders</button>
            </div>
        </div>
    );
}

export default StudentDashboard;