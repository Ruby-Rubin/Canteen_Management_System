import "./Login.css";

function Login() {
    return (
        <div className="login-container">
            <h1>College Canteen System</h1>

            <h2>Student Login</h2>

            <input
                type="text"
                placeholder="Register Number"
            />

            <br /><br />

            <input
                type="password"
                placeholder="Password"
            />

            <br /><br />

            <button>Login</button>
        </div>
    );
}

export default Login;