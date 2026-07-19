import { Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import StudentDashboard from "./pages/StudentDashboard";
import OrderMenu from "./pages/OrderMenu";
function App() {
    return (
        <Routes>
            <Route path="/" element={<Login />} />
            <Route path="/student" element={<StudentDashboard />} />
            <Route path="/order/:session_id" element={<OrderMenu />} />
        </Routes>
    );
}``

export default App;