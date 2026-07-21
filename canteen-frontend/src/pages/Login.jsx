import "./Login.css";
import {useState} from "react"; 
import axios from 'axios';
import { useNavigate } from "react-router-dom";

function Login() {
    const [registerNo,setRegisterNo]=useState("");
    const [password, setPassword]=useState("");
    const [showPopup, setShowPopup] = useState(false);

const [popupMessage, setPopupMessage] = useState("");
    const navigate = useNavigate();
   async function handleLogin() {

    

    try {

        const response = await axios.post(
            "http://127.0.0.1:5000/login",
            {
                register_no: registerNo,
                password: password
            }
        );
        
       if (response.data.success) {
    console.log(response.data);
    localStorage.setItem("user", JSON.stringify(response.data));
    navigate("/student");
}
} catch (error) {
    setPopupMessage(error.response.data.message);
    setShowPopup(true);
    console.log(error.response.data);
}
}

return (
        <div className="login-container">

            <div className="login-card">

                <h1>🍽 College Canteen System</h1>

                <h2>Student Login</h2>
                <p> Welcome Back!!, Please Sign-in to continue</p>

                <input
                    type="text"
                    placeholder="Register Number"
                    value={registerNo}
                    onChange={(e)=>setRegisterNo(e.target.value)}
                />

                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e)=>setPassword(e.target.value)}
                />

                <button onClick={handleLogin}>
                    Login
                </button>

            </div>
            {showPopup && (
                <div className="popup-overlay">
                    <div className="popup">

                    <h3>Error</h3>

                    <p>{popupMessage}</p>

                    <button
                        onClick={() => setShowPopup(false)}
                    >
                        OK
                    </button>

                    </div>
                </div>
            )}
            </div>
         );
}


export default Login;