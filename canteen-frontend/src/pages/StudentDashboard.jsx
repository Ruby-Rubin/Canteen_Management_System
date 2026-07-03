import { useLocation } from "react-router-dom";

function StudentDashboard() {

    const location = useLocation();
    const user = location.state.user;

    return (
        <div>
            <h1>Welcome, {user.name} 👋</h1>

            <p>Register Number: {user.register_no}</p>

            <p>Role: {user.role}</p>
        </div>
    );
}

export default StudentDashboard;