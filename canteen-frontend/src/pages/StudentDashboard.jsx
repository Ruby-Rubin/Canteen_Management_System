import { useLocation } from "react-router-dom";
import "./StudentDashboard.css";

function StudentDashboard() {

    const location = useLocation();
    const user = location.state.user;

    return (
        <div className='student-dashboard'>
            <div className="dashboard-card">
            <h1>Welcome, {user.name} 👋</h1>
            <p className="meal-active">Lunch is Active</p>
            <button className="order-now">Order Now</button>
            <button className='pre-order'>Pre-Order</button>
            <button className='cart'>Cart</button>
            <button className='my-orders'>My Orders</button>
            </div>
        </div>
    );
}

export default StudentDashboard;