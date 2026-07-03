import "./Login.css";
import {useState} from "react"; 

function Login() {
    const [registerNo,setRegisterNo]=useState("");
    const [password, setPassword]=useState("");
    function handleLogin() {

    console.log("Register No:", registerNo);
    console.log("Password:", password);

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

        </div>
    );
}

export default Login;